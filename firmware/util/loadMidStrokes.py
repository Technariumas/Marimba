#!/usr/bin/python
import pickle
from marimba import Marimba
m=Marimba()
m.connect()

try:
	with open('/home/pi/Marimba/firmware/util/midStroke', 'rb') as fp:
		midStroke = pickle.load(fp)
except Exception:
	midStroke = [17] * 80
print ("Loading MIDDLE stroke strengths:")
print ([(m.setMidStrokeLength(n, midStroke[n], test=False), n, midStroke[n]) for n in range(80)])
