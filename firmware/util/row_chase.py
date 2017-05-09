#!/usr/bin/python
from marimba import Marimba
import time
import numpy as np

m = Marimba()
m.connect()

print("Rolling rows...")
index_array = np.reshape(np.arange(80), (8, 10)).T
while True:
	for row in index_array:
		m.playSequence(row, 0, 0.5)
		time.sleep(0.25)
	time.sleep(2)

