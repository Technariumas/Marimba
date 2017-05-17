#!/usr/bin/python
from marimba import Marimba
import time
import numpy as np

m = Marimba()
m.connect()

print("Rolling columns...")
index_array = np.reshape(np.arange(80), (8, 10)).T


while True:
		notes = [13, 14, 15, 16, 17, 18, 19]
		#notes, delay, duration
		m.playSequence(notes, 0.001, 0.25)
		time.sleep(0.5)
		time.sleep(1)

