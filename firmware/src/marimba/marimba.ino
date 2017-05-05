#include <inttypes.h>
#include <Bounce2.h>

#include "pca9685.h"
#include <MIDI.h>
#include "myserial.h"

#define BUTTON1 13
#define BUTTON2 11

#define SOLENOID1 9  
#define SOLENOID2 10

#define STICK SOLENOID1
#define DAMPER SOLENOID2

#define POT1 A0
#define POT2 A1

struct MarimbaMIDISettings : public midi::DefaultSettings {
	static const unsigned SysExMaxSize = 1; // Accept SysEx messages up to 1 bytes long.
	static const long BaudRate = 9600;
};

#define SERIAL_RX_BUFFER_SIZE 8
typedef uint8_t rx_buffer_index_t;

MIDI_CREATE_CUSTOM_INSTANCE(MySerial, mySerial, MIDI, MarimbaMIDISettings);

Bounce button1 = Bounce();
Bounce button2 = Bounce();

inline static void buttonsSetup() {
	pinMode(BUTTON1, INPUT);
	pinMode(BUTTON2, INPUT);

	button1.attach(BUTTON1);
	button1.interval(100);

	button2.attach(BUTTON2);
	button2.interval(100);
}

inline static void outputsSetup() {
	pinMode(SOLENOID1, OUTPUT);
	pinMode(SOLENOID2, OUTPUT);
}

PCA9685_Init_TypeDef PCA9685_Params = {
	.Address = 0x40,
	.InvOutputs = PCA9685_NotInvOutputs,
	.OutputDriver = PCA9685_OutputDriver_TotemPole,
	.OutputNotEn = PCA9685_OutputNotEn_OUTDRV,
	.PWMFrequency = PCA9685_Frequency_200Hz
};

void ledsOff() {
	for(uint8_t i = 10; i < 16; i++) {
		PCA9685_SetOutput(0x40, i, 4095);
	}	
}

void setLed2() {
	PCA9685_SetOutput(0x40, 10, 4095);
	PCA9685_SetOutput(0x40, 11, 0);
	PCA9685_SetOutput(0x40, 12, 4095);
}

void setLed1() {
	PCA9685_SetOutput(0x40, 13, 4095);
	PCA9685_SetOutput(0x40, 14, 4095);
	PCA9685_SetOutput(0x40, 15, 0);
}

inline static ledDriverSetup() {
	PCA9685_Init(&PCA9685_Params);
	ledsOff();
	delay(300);
	setLed1();
	delay(300);
	setLed2();
	delay(300);
	ledsOff();
}

static inline void midiSetup() {
    MIDI.setHandleNoteOn(handleNoteOn);  // Put only the name of the function
    MIDI.setHandleNoteOff(handleNoteOff);
    MIDI.setHandleControlChange(handleControlChange);
    MIDI.begin(MIDI_CHANNEL_OMNI);
}

static inline uint16_t getDipSwitch() {
	uint16_t result = 0;
    PORTC |= _BV(PC2);
    PORTC |= _BV(PC3);
    PORTD |= _BV(PD1);
    PORTD |= _BV(PD2);
    PORTD |= _BV(PD3);
    PORTD |= _BV(PD4);
    PORTD |= _BV(PD5);
    PORTD |= _BV(PD6);
    PORTD |= _BV(PD7);
    PORTB |= _BV(PB0);

	result = result | ((0 == (_BV(PINC2) & PINC)) << 0);
	result = result | ((0 == (_BV(PINC3) & PINC)) << 1);
	result = result | ((0 == (_BV(PIND1) & PIND)) << 2);
	result = result | ((0 == (_BV(PIND2) & PIND)) << 3);
	result = result | ((0 == (_BV(PIND3) & PIND)) << 4);
	result = result | ((0 == (_BV(PIND4) & PIND)) << 5);
	result = result | ((0 == (_BV(PIND5) & PIND)) << 6);
	result = result | ((0 == (_BV(PIND6) & PIND)) << 7);
	result = result | ((0 == (_BV(PIND7) & PIND)) << 8);
	result = result | ((0 == (_BV(PINB0) & PINB)) << 9);

	return result;
}

void setup(){
	ledDriverSetup();
	buttonsSetup();
	outputsSetup();
	midiSetup();
	TCCR1B = TCCR1B & 0b11111000 | 1;
}

uint16_t lights[] = {4095, 4095, 4095, 4095, 500, 500, 500, 500};
uint8_t tail = 0, head = 4;

void outputLights() {
  for(uint8_t i = 0; i < 8; i++) {
  	PCA9685_SetOutput(0x40, i, ((uint32_t)lights[i] * (uint32_t)lights[i])/4095);
  }
}

uint8_t step = 12;
uint16_t minimum = 500;
uint16_t maximum = 4095;

static inline void setLedCount(uint8_t count) {
  uint8_t i;

  if(count > 7) {
    count = 7;
  }
  if(count < 1) {
    count = 1;
  }
  int8_t prevCount = head - tail;
  uint8_t newHead = (tail + count) % 8;

  if(prevCount < 0) {
    prevCount += 8;
  }

  if(count > prevCount) {
    lights[newHead] = lights[head];
    for(i = 0; i < (count - prevCount); i++){
      lights[(head + i)%8] = maximum;
    }
  } else if(count < prevCount) {
    lights[newHead] = lights[head];
    for(i = 0; i < prevCount - count; i++) {
      lights[(newHead + 1 + i) % 8] = minimum;
    }
  }

  head = newHead;
}

  void initLights() {
  for(int i = 0; i < 8; i++) {
    if(head > tail){
      if(i < tail) {
        lights[i] = minimum;
      } else if(i >= tail && i < head) {
        lights[i] = maximum;
      } else if(i >= head) {
        lights[i] = minimum;
      }
    } else {
      if(i < tail && i >= head) {
        lights[i] = minimum;
      } else if(i >= tail) {
        lights[i] = maximum;
      } else if(i < head) {
        lights[i] = maximum;
      }
    }
    
  }
}

void chase() {
	if(lights[head] + step <= maximum) {
		lights[head] += step;
		
		if(lights[tail] - step > minimum) {
			lights[tail] -= step;
		}
		outputLights();
	} else {
		head = (head + 1) % 8;
		tail = (tail + 1) % 8;
	}
}

uint8_t myNote = 0;

void loop() {
	myNote = getDipSwitch();
	chase();
	button1.update();
	button2.update();
	MIDI.read();
	if(button1.fell()) {
		strokeHigh();
	}
	if(button2.fell()) {
		dampen();
	}
}

void strokeHigh() {
  analogWrite(STICK, 255);
  delay(19);
  digitalWrite(STICK, LOW);
}

void strokeMid() {
  analogWrite(STICK, 255);
  delay(1);
  analogWrite(STICK, 128);
  delay(60);
  digitalWrite(STICK, LOW);
}

void dampen() {
  for(uint8_t i = 0; i <=128; i+=2) {
    analogWrite(DAMPER, i);
    delay(5);  
  }
  delay(200);
  for(uint8_t i = 128; i > 40; i-=2) {
    analogWrite(DAMPER, i);
    delay(5);  
  }
//  delay(100);
  analogWrite(DAMPER, 0);
}

#define CHANNEL_SOLENOIDS 1
#define CHANNEL_PARAM_LED_STEP 2
#define CHANNEL_PARAM_LED_MINIMUM 3
#define CHANNEL_PARAM_LED_MAXIMUM 4
#define CHANNEL_PARAM_LED_COUNT 5

void handleNoteOn(byte channel, byte pitch, byte velocity) {
	if(myNote == pitch) {
		setLed1();
		switch(channel) {
			case CHANNEL_SOLENOIDS:
				if(127 == velocity) {
					strokeHigh();
				} else if(0 == velocity) {
					dampen();
				} else {
					strokeMid();
				}
				break;
			case CHANNEL_PARAM_LED_STEP:
				step = velocity;
				break;
			case CHANNEL_PARAM_LED_MINIMUM:
				minimum = velocity * 32;
				break;
			case CHANNEL_PARAM_LED_MAXIMUM:
				maximum = velocity * 32;
				break;
			case CHANNEL_PARAM_LED_COUNT:
				setLedCount(velocity);
				break;
		}
	}
}

void handleNoteOff(byte channel, byte pitch, byte velocity) {
	if(myNote == pitch) {
		ledsOff();
		dampen();
	}
}

void handleControlChange(byte channel, byte pitch, byte velocity) {
	setLed2();
}

