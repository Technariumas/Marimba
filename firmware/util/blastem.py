#!/usr/bin/python
from marimba import Marimba
import time

m = Marimba()
m.connect()
while True:
	m.play(2)
	time.sleep(0.1)
