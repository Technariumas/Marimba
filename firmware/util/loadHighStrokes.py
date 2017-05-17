#!/usr/bin/python
import pickle
from marimba import Marimba
m=Marimba()
m.connect()

try:
	with open('/home/pi/Marimba/firmware/util/highStroke', 'rb') as fp:
		highStroke = pickle.load(fp)
except EOFError:
	highStroke = [17] * 80
print ("Loading HIGH stroke strengths:")
print ([(m.setHighStrokeLength(n, highStroke[n], test=False), n, highStroke[n]) for n in range(80)])
