#!/usr/bin/python
from marimba import Marimba
from time import sleep
from os import sys

box_number = sys.argv[1]
m = Marimba()
m.connect()

print("Blasting some MIDI notes...")
while True:
	m.play(box_number, 127)
	sleep(0.5)
	m.stop(box_number)
	sleep(2)
	m.stop(box_number)
#	m.play(0, 64)
#	sleep(0.1)
#	m.play(0, 64)
#	sleep(2)
