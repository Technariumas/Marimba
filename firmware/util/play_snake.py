#!/usr/bin/python
from marimba import Marimba
import time

m = Marimba()
m.connect()

print("Playing boxes 0-79...")
while True:
	m.playAll([x for x in range(80)])
	time.sleep(5)

