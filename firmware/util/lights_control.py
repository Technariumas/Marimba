
from marimba import Marimba
from random import randrange
from time import sleep
import numpy as np

m = Marimba()
m.connect()

[m.setLightStep(n, 3) for n in range(80)]
sleep(1)
[m.setLightCount(n, 4) for n in range(80)]
sleep(1)
[m.setLightMinimum(n, 15) for n in range(80)]
sleep(1)

[m.setLightMaximum(n, 127) for n in range(80)]
sleep(1)
#[m.setLightMaximum(n, 60) for n in [randrange(60, 80) for i in range(3)]]
#sleep(1)
#[m.setLightMaximum(n, 80) for n in [randrange(20, 60) for i in range(7)]]
#sleep(1)
#[m.setLightMaximum(n, 60) for n in [randrange(0, 10) for i in range(3)]]

index_array = np.arange(80)
index_array = np.reshape(index_array, (8, 10)).T

wall_lights = index_array[np.where((index_array <= 10) | (index_array >= 60))]


def get_lowest_max_brightness(box):
	if box in wall_lights:
		return 60
 	else:
		return 80

def flash_lights(boxes):
	current_max_brightness = 127
	while current_max_brightness > get_lowest_max_brightness(box) :
		m.setLightMaximum(box, current_max_brightness)
		print current_max_brightness
		current_max_brightness-=4
		sleep(0.1)
	sleep(10)
	while current_max_brightness <= 123:
		m.setLightMaximum(box, current_max_brightness)
		print current_max_brightness
		current_max_brightness+=4
		sleep(0.1)
	sleep(10)

for i, tone in enumerate([0, 2, 5, 7]):
	for i, octave in enumerate([3, 4, 5, 6]):
		current_boxes = index_array(get_boxes(tone, octave)
		flash_lights(current_boxes)
			

