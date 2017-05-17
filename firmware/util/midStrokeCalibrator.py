#!/usr/bin/python
import pickle
from marimba import Marimba
m=Marimba()
m.connect()

try:
	with open('midStroke', 'rb') as fp:
		midStroke = pickle.load(fp)
except EOFError:
	midStroke = [60] * 80

for n in range(80):
	print("Dabartine jega: " + str(midStroke[n]))
	m.setMidStrokeLength(n, midStroke[n])
	while True:
		key = raw_input("Patiko? (T/N)")
		if 'T' == key or 't' == key:
			with open('midStroke', 'wb') as fp:
				pickle.dump(midStroke, fp)
			break
		else:
			val = raw_input("Ivesk smugio jega [0 - 127] gera pradzia - 60:")
			try:
				i = int(val)
				if i >= 0 and i <= 127:
					midStroke[n] = i
					m.setHighStrokeLength(n, i)
			except ValueError:
				print("Vesk tik skaicius!")
				m.test(n)
