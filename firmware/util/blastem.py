#!/usr/bin/python
from marimba import Marimba
import time

m = Marimba()
m.connect()

print("Blasting some MIDI notes...")
while True:
	m.play(2)
	time.sleep(0.5)
	m.stop(2)
	time.sleep(2)
