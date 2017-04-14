


#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

void setup() {
  Serial.begin(9600);
  Serial.println("16 channel PWM test!");

  // if you want to really speed stuff up, you can go into 'fast 400khz I2C' mode
  // some i2c devices dont like this so much so if you're sharing the bus, watch
  // out for this!

  pwm.begin();
  pwm.setPWMFreq(1600);  // This is the maximum PWM frequency
    
  // save I2C bitrate
  uint8_t twbrbackup = TWBR;
  // must be changed after calling Wire.begin() (inside pwm.begin())
  TWBR = 12; // upgrade to 400KHz!

//  pwm.setPWM(8, 0, 4095);
//  delay(500);
  pwm.setPWM(8, 0, 0);
    
}

uint16_t lights[] = {4095, 4095, 4095, 4095, 500, 500, 500, 500};
uint8_t tail = 0, head = 4;

void outputLights() {
  for(uint8_t i = 0; i < 8; i++) {
    pwm.setPWM(i, 0, ((uint32_t)lights[i] * (uint32_t)lights[i])/4095);
  }
}

uint8_t step = 12;
int minimum = 500;

uint32_t lastPrr= 0;

void chase() {
    if(lights[head] + step <= 4095) {
    lights[head] += step;
    if(lights[tail] - step > minimum) {
      lights[tail] -= step;
    }
    outputLights();
  } else {
    head = (head + 1) % 8;
    tail = (tail + 1) % 8;
//    if(step > 10) {
//      step--;
//    } else {
//      step = 200;
//    }
  }
}

void loop() {
  chase();
//    outputLights();
//  if(millis()- lastPrr > 300) {
//    pwm.setPWM(8, 0, 4095);
//    delay(50);
//    pwm.setPWM(8, 0, 0);
//    lastPrr = millis();    
//  }
}
