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
    lights[tail] = minimum;
    lights[head] = maximum;
		head = (head + 1) % 8;
		tail = (tail + 1) % 8;
	}
}
