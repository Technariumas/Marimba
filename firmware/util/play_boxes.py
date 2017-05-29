#!/usr/bin/python
from marimba import Marimba
import time
import sys

volume = int(sys.argv[1])

m = Marimba()
m.connect()

print("Playing boxes 0-79...")
while True:
	#notes, delay, duration, velocity
	m.playSequence([x for x in range(80)], 1, 2, volume)
	time.sleep(5)
