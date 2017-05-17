#!/usr/bin/python
import pickle
from marimba import Marimba
m=Marimba()
m.connect()

try:
	with open('highStroke', 'rb') as fp:
		highStroke = pickle.load(fp)
except EOFError:
	highStroke = [17] * 80
print ("Loading HIGH stroke strengths:")
print ([(m.setHighStrokeLength(n, highStroke[n]), n, highStroke[n]) for n in range(80)])