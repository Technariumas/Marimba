#!/usr/bin/python
from marimba import Marimba
import time
import numpy as np

m = Marimba()
m.connect()

print("Rolling columns...")
index_array = np.reshape(np.arange(80), (8, 10)).T
while True:
	m.play([2, 3, 4])
	time.sleep(0.5)
	m.stop(2)
	time.sleep(2)

