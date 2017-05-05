#include <inttypes.h>
#include <Bounce2.h>
#include <avr/delay.h>

#include "pca9685.h"
#include <MIDI.h>
#include "myserial.h"
#include "lights.h"

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
	// pinMode(BUTTON1, INPUT);
	// pinMode(BUTTON2, INPUT);

	button1.attach(BUTTON1);
	button1.interval(100);

	button2.attach(BUTTON2);
	button2.interval(100);
}

inline static void outputsSetup() {
	DDRB |= _BV(PB1) | _BV(PB2);	
	// pinMode(SOLENOID1, OUTPUT);
	// pinMode(SOLENOID2, OUTPUT);
}

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
	PCA9685_Init();
	ledsOff();
	_delay_ms(300);
	setLed1();
	_delay_ms(300);
	setLed2();
	_delay_ms(300);
	ledsOff();
}

static inline void midiSetup() {
    MIDI.setHandleNoteOn(handleNoteOn);  // Put only the name of the function
    MIDI.setHandleNoteOff(handleNoteOff);
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


uint8_t myNote = 0;

uint32_t strokeEnd = 0;
uint8_t strokeHighLength = 17;
uint8_t strokeMidLength = 60;
uint8_t strokeInProgress = 0;

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
		startDamper();
	}
	
	if(strokeInProgress && (millis()  > strokeEnd)) {
		TCCR1A &= ~_BV(COM1A1);
		PORTB &= ~_BV(PB1);
		// digitalWrite(STICK, LOW);
		strokeInProgress = 0;
	}
	dampen();
}

void strokeHigh() {
	PORTB |= _BV(PB1);	
	// analogWrite(STICK, 255);
	strokeEnd = millis() + strokeHighLength;
	strokeInProgress = 1;
  // _delay_ms(19);
  // digitalWrite(STICK, LOW);
}

void strokeMid() {
	PORTB |= _BV(PB1);	
	//analogWrite(STICK, 255);
	_delay_ms(1);
	
	TCCR1A |= _BV(COM1A1);
	OCR1A = 128;
//	analogWrite(STICK, 128);
	strokeInProgress = 1;
	strokeEnd = millis() + strokeMidLength;
	// _delay_ms(60);
	// digitalWrite(STICK, LOW);
}

#define DAMPEN_IDLE 		0
#define DAMPEN_ENGAGE 		1
#define DAMPEN_PRESS 		2
#define DAMPEN_DISENGAGE 	3

uint8_t dampenPhase = DAMPEN_IDLE;
uint32_t dampenCycleEnd = 0;
uint8_t damperDrive = 0;

uint8_t dampenCycleLength = 3;
uint16_t dampenPressLength = 300;
uint8_t damperMaxDrive = 128;

uint8_t isDamperIdle() {
	return 0 == dampenPhase;
}

void dampen() {
	switch(dampenPhase) {
		case DAMPEN_ENGAGE:
			if(millis() > dampenCycleEnd) {
				damperDrive += 1;
				OCR1B = damperDrive;
				// analogWrite(DAMPER, damperDrive);
				if(damperDrive >= damperMaxDrive){
					dampenPhase = DAMPEN_PRESS;
					dampenCycleEnd = millis() + dampenPressLength;
				} else {
					dampenCycleEnd = millis() + dampenCycleLength;
				}
			}
			break;
		case DAMPEN_PRESS:
			if(millis() > dampenCycleEnd) {
				dampenPhase = DAMPEN_DISENGAGE;
				dampenCycleEnd = millis() + dampenCycleLength;
			}
			break;
		case DAMPEN_DISENGAGE:
			if(millis() > dampenCycleEnd) {
				damperDrive -= 1;
				OCR1B = damperDrive;
				// analogWrite(DAMPER, damperDrive);

				if(damperDrive <= 0){
					dampenPhase = DAMPEN_IDLE;
				} else {
					dampenCycleEnd = millis() + dampenCycleLength;
				}
			}
			break;
	}
}

void startDamper() {
	dampenPhase = DAMPEN_ENGAGE;
	dampenCycleEnd = millis() + dampenCycleLength;
    damperDrive = 1;
	TCCR1A |= _BV(COM1B1);
	OCR1B = damperDrive;
//    analogWrite(DAMPER, damperDrive);
//   for(uint8_t i = 0; i <=128; i+=2) {
//     analogWrite(DAMPER, i);
//     _delay_ms(2);  
//   }
//   _delay_ms(300);
//   for(uint8_t i = 128; i > 40; i-=2) {
//     analogWrite(DAMPER, i);
//     _delay_ms(2);  
//   }
// //  _delay_ms(100);
//   analogWrite(DAMPER, 0);
}

#define CHANNEL_SOLENOIDS 1
#define CHANNEL_PARAM_LED_STEP 2
#define CHANNEL_PARAM_LED_MINIMUM 3
#define CHANNEL_PARAM_LED_MAXIMUM 4
#define CHANNEL_PARAM_LED_COUNT 5
#define CHANNEL_PARAM_STROKE_HIGH_LENGTH 6
#define CHANNEL_PARAM_STROKE_MID_LENGTH 7
#define CHANNEL_PARAM_DAMPER_ENGAGE_DELAY 8
#define CHANNEL_PARAM_DAMPER_PRESS_LENGTH 9
#define CHANNEL_PARAM_DAMPER_MAX_DRIVE 10

void handleNoteOn(byte channel, byte pitch, byte velocity) {
	if(myNote == pitch) {
		setLed1();
		switch(channel) {
			case CHANNEL_SOLENOIDS:
				if(127 == velocity && !strokeInProgress && isDamperIdle()) {
					strokeHigh();
				} else if(0 == velocity) {
					startDamper();
				} else if(!strokeInProgress && isDamperIdle()) {
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
			case CHANNEL_PARAM_STROKE_HIGH_LENGTH:
				strokeHighLength = velocity;
				break;
			case CHANNEL_PARAM_STROKE_MID_LENGTH:
				strokeMidLength = velocity;
				break;
			case CHANNEL_PARAM_DAMPER_ENGAGE_DELAY:
				dampenCycleLength = velocity;
				break;
			case CHANNEL_PARAM_DAMPER_PRESS_LENGTH:
				dampenPressLength = velocity;
				break;
			case CHANNEL_PARAM_DAMPER_MAX_DRIVE:
				damperMaxDrive = velocity;
				break;
		}
	}
}

void handleNoteOff(byte channel, byte pitch, byte velocity) {
	if(myNote == pitch && isDamperIdle()) {
		ledsOff();
		startDamper();
	}
}

