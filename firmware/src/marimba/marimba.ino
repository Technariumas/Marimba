#include <inttypes.h>
// #include <Bounce2.h>
#include <avr/delay.h>

#include "pca9685.h"
#include <MIDI.h>

#define HEALTH_GOOD 		0
#define HEALTH_IN_NOTE 		_BV(1)
#define HEALTH_NO_MIDI 		_BV(2)
#define HEALTH_NO_HAMMER 	_BV(3)
#define HEALTH_NO_DAMPER 	_BV(4)

uint8_t healthStatus = 0;
#define SERIAL_RX_BUFFER_SIZE 240

#include "myserial.h"
#include "lights.h"

#define BUTTON1 13
#define BUTTON2 11

#define SOLENOID1 9  
#define SOLENOID2 10

#define HAMMER SOLENOID1
#define DAMPER SOLENOID2

#define POT1 A0
#define POT2 A1

#define HAMMER_SENSE A7
#define DAMPER_SENSE A6

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



uint32_t lastMidiTs = 0;

struct MarimbaMIDISettings : public midi::DefaultSettings {
	static const unsigned SysExMaxSize = 1; // Accept SysEx messages up to 1 bytes long.
	static const long BaudRate = 9600;
};

typedef uint8_t rx_buffer_index_t;

MIDI_CREATE_CUSTOM_INSTANCE(MySerial, mySerial, MIDI, MarimbaMIDISettings);

// Bounce button1 = Bounce();
// Bounce button2 = Bounce();

inline static void buttonsSetup() {
	 pinMode(BUTTON1, INPUT);
	 pinMode(BUTTON2, INPUT);

	// button1.attach(BUTTON1);
	// button1.interval(100);

	// button2.attach(BUTTON2);
	// button2.interval(100);
}

inline static void outputsSetup() {
	DDRB |= _BV(PB1) | _BV(PB2);	
	// pinMode(SOLENOID1, OUTPUT);
	// pinMode(SOLENOID2, OUTPUT);
}

// void ledsOff() {
// 	for(uint8_t i = 10; i < 16; i++) {
// 		PCA9685_SetOutput(0x40, i, 4095);
// 	}	
// }

#define LED1 10
#define LED2 13

void setLed(uint8_t led, uint16_t r, uint16_t g, uint16_t b) {
	PCA9685_SetOutput(0x40, led,   r);
	PCA9685_SetOutput(0x40, led+1, g);
	PCA9685_SetOutput(0x40, led+2, b);
}

inline static ledDriverSetup() {
	PCA9685_Init();
//	setLed(LED1, 0, 4095, 4095);
	setLed(LED1, 0, 4095, 4095);
	_delay_ms(500);
	setLed(LED2, 4095, 4095, 0);
//	setLed(LED2, 4095, 4095, 0);
	_delay_ms(500);
	// setLed(LED1, 4095, 3500, 4095);
	setLed(LED2, 4095, 4095, 4095);
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
	outputsSetup();
	midiSetup();
	TCCR1B = TCCR1B & 0b11111000 | 1;
    OCR1A = 0;
	TCCR1A |= _BV(COM1A1);

	buttonsSetup();
}


uint8_t myNote = 0;

uint32_t strokeEnd = 0;
uint8_t strokeHighLength = 17;
uint8_t strokeMidLength = 60;
uint8_t strokeInProgress = 0;



inline static void displayHealth() {
	if(HEALTH_GOOD == healthStatus || HEALTH_NO_MIDI == healthStatus) {
		setLed(LED1, 4095, 3500, 4095);
		return;
	}

	if(healthStatus & HEALTH_NO_HAMMER) {
		setLed(LED1, 0, 4095, 4095);
		return;
	}

	if(healthStatus & HEALTH_NO_DAMPER) {
		setLed(LED1, 1000, 4095, 1000);
		return;
	}

	if(healthStatus & HEALTH_NO_MIDI) {
		setLed(LED2, 4095, 4095, 0);
	} else {
		setLed(LED2, 4095, 4095, 4095);
	}

	if(healthStatus & HEALTH_IN_NOTE) {
		setLed(LED1, 4095, 0, 4095);
	}
}


void loop() {
	myNote = getDipSwitch();
	chase();
    // _delay_ms(2);
	// button1.update();
	// button2.update();

	MIDI.read();
	
	// if(button1.fell()) {
	// 	strokeHigh();
	// }
	// if(button2.fell()) {
	// 	startDamper();
	// }

    if( !strokeInProgress && ((PINB & _BV(PINB5))==0) )
        { 
            handleNoteOn(CHANNEL_SOLENOIDS, myNote, 127);

        setLed(LED1, 4095, 0, 4095);
        }
        else setLed(LED1, 4095, 4095, 4095);

    if( !strokeInProgress && ((PINB & _BV(PINB3))==0 )) 
        { 
            handleNoteOn(CHANNEL_SOLENOIDS, myNote, 64);

        setLed(LED1, 4095, 0, 4095);
        }
        else setLed(LED1, 4095, 4095, 4095);

    if( strokeInProgress)
     {
        setLed(LED2, 4095, 4095, 0);
     }
    else
     {   
        setLed(LED2, 4095, 4095, 4095);
     };
	
	if(strokeInProgress && (millis()  > strokeEnd)) {
	//	TCCR1A &= ~_BV(COM1A1);
	//	PORTB |=_BV(PB1);
//		if(analogRead(HAMMER_SENSE) < 50) {
			// healthStatus |= HEALTH_NO_HAMMER;
//		} else {
			// healthStatus &= ~HEALTH_NO_HAMMER;
//		}
	//	PORTB &= ~_BV(PB1);
		// digitalWrite(HAMMER, LOW);
    	OCR1A = 0;
		strokeInProgress = 0;
	}
	dampen();
	if(millis() - lastMidiTs > 5000) {
		healthStatus |= HEALTH_NO_MIDI;
	} else {
		healthStatus &= ~HEALTH_NO_MIDI;
	}

	displayHealth();
}

void strokeHigh() {
//	PORTB |= _BV(PB1);
	OCR1A = 255;
	// analogWrite(HAMMER, 255);
	strokeEnd = millis() + strokeHighLength;
	strokeInProgress = 1;
  // _delay_ms(19);
  // digitalWrite(HAMMER, LOW);
}

void strokeMid() {
//	PORTB |= _BV(PB1);	
	//analogWrite(HAMMER, 255);
	_delay_ms(1);
	
//	TCCR1A |= _BV(COM1A1);
	OCR1A = 128;
//	analogWrite(HAMMER, 128);
	strokeInProgress = 1;
	strokeEnd = millis() + strokeMidLength;
	// _delay_ms(60);
	// digitalWrite(HAMMER, LOW);
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
	return DAMPEN_IDLE == dampenPhase;
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
				OCR1B = 255;
				_delay_us(10);
				if(analogRead(DAMPER_SENSE) < 50) {
					healthStatus |= HEALTH_NO_DAMPER;
				} else {
					healthStatus &= ~HEALTH_NO_DAMPER;
				}
				OCR1B = damperMaxDrive;
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
	healthStatus &= ~HEALTH_IN_NOTE;
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

void handleNoteOn(byte channel, byte pitch, byte velocity) {
	lastMidiTs = millis();

	if(0 == velocity && 1 == channel) {
		handleNoteOff(channel, pitch, velocity);
		return;
	}
	if(myNote == pitch) {
		switch(channel) {
			case CHANNEL_SOLENOIDS:
				if(127 == velocity && !strokeInProgress && isDamperIdle()) {
					healthStatus |= HEALTH_IN_NOTE;
					strokeHigh();
				} else if(!strokeInProgress && isDamperIdle()) {
					healthStatus |= HEALTH_IN_NOTE;
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
				dampenPressLength = velocity * 3;
				break;
			case CHANNEL_PARAM_DAMPER_MAX_DRIVE:
				damperMaxDrive = velocity * 2;
				break;
		}
	}
}

void handleNoteOff(byte channel, byte pitch, byte velocity) {
	lastMidiTs = millis();
	if(myNote == pitch && isDamperIdle()) {
		startDamper();
	}
}

