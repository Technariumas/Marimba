#!/usr/bin/python

from marimba import Marimba
from random import randrange
from time import sleep
import numpy as np
from note_mapping import get_note

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
	while current_max_brightness >  60:
		for box in boxes:
			if get_lowest_max_brightness(box) > current_max_brightness:
				continue
			else:
				m.setLightMaximum(box, current_max_brightness)
		current_max_brightness-=2
		sleep(1)
	sleep(4.6)
	while current_max_brightness <= 123:
		for box in boxes:
			m.setLightMaximum(box, current_max_brightness)
		current_max_brightness+=2
		sleep(1)
	sleep(4.6)

octaves = [3, 4, 5, 6] 
while True:

	for i, tone in enumerate([0, 2, 5, 7]):
		current_boxes = index_array[get_note(tone)]
		flash_lights(current_boxes)
			

