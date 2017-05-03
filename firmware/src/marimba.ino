#include <inttypes.h>
#include <Wire.h>
#include <Bounce2.h>
#include <Adafruit_PWMServoDriver.h>

#define BUTTON1 13
#define BUTTON2 11
#define SOLENOID1 9  
#define SOLENOID2 10
#define POT1 A0
#define POT2 A1

Bounce button1 = Bounce();
Bounce button2 = Bounce();
Adafruit_PWMServoDriver leds = Adafruit_PWMServoDriver();

inline static void buttonsSetup() {
	pinMode(BUTTON1, INPUT);
	pinMode(BUTTON2, INPUT);

	button.attach(BUTTON1);
	button.interval(100);

	button.attach(BUTTON2);
	button.interval(100);
}


inline static void outputsSetup() {
	pinMode(SOLENOID1, OUTPUT);
	pinMode(SOLENOID2, OUTPUT);
}

inline static ledDriverSetup() {
  leds.begin();
  leds.setPWMFreq(1600);  // This is the maximum PWM frequency
    
  // save I2C bitrate
  uint8_t twbrbackup = TWBR;
  // must be changed after calling Wire.begin() (inside pwm.begin())
  TWBR = 12; // upgrade to 400KHz!

  leds.setPWM(8, 0, 0);
}

uint16_t getDipSwitch() {
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

	result = result | ((0 == (_BV(PINC2) | PINC)) << 0);
	result = result | ((0 == (_BV(PINC3) | PINC)) << 1);
	result = result | ((0 == (_BV(PIND1) | PIND)) << 2);
	result = result | ((0 == (_BV(PIND2) | PIND)) << 3);
	result = result | ((0 == (_BV(PIND3) | PIND)) << 4);
	result = result | ((0 == (_BV(PIND4) | PIND)) << 5);
	result = result | ((0 == (_BV(PIND5) | PIND)) << 6);
	result = result | ((0 == (_BV(PIND6) | PIND)) << 7);
	result = result | ((0 == (_BV(PIND7) | PIND)) << 8);
	result = result | ((0 == (_BV(PINB0) | PINB)) << 9);

	return result;
}

void setup(){
	buttonsSetup();
	outputsSetup();
}

void loop() {
	button1.update();
	button2.update();
}