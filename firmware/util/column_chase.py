#!/usr/bin/python
from marimba import Marimba
import time
import numpy as np

m = Marimba()
m.connect()

print("Rolling columns...")
index_array = np.reshape(np.arange(80), (8, 10)).T

while True:
	for i in range(index_array.shape[1]):
		#notes, delay, duration
		m.playSequence(index_array[:,i], 0.01, 1)
		time.sleep(0.25)
	time.sleep(1)

