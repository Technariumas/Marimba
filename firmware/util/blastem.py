#!/usr/bin/python
from marimba import Marimba
from time import sleep


m = Marimba()
m.connect()

print("Blasting some MIDI notes...")
while True:
	m.setLightCount(127, 1)
	sleep(0.1)
	m.setLightCount(127, 4)
	sleep(0.1)
