#!/usr/bin/python
import pickle
from marimba import Marimba
import sys

m=Marimba()
m.connect()

box_number = sys.argv[1]

try:
	with open('highStroke', 'rb') as fp:
		highStroke = pickle.load(fp)
except EOFError:
	highStroke = [17] * 80


if box_number == "all":
	for n in range(80):
		print("Dabartine jega: " + str(highStroke[n]))
		m.setHighStrokeLength(n, highStroke[n])
		while True:
			key = raw_input("Patiko? (T/N)")
			if 'T' == key or 't' == key:
				with open('highStroke', 'wb') as fp:
					pickle.dump(highStroke, fp)
				break
			else:
				val = raw_input("Ivesk smugio jega [0 - 127] gera pradzia - 17:")
				try:
					i = int(val)
					if i >= 0 and i <= 127:
						highStroke[n] = i
						m.setHighStrokeLength(n, i)
				except ValueError:
					print("Vesk tik skaicius!")
					m.test(n)
else:
	n = int(box_number)
	print("Dabartine jega: " + str(highStroke[n]))
	m.setHighStrokeLength(n, highStroke[n])
	while True:
			key = raw_input("Patiko? (T/N)")
			if 'T' == key or 't' == key:
				with open('highStroke', 'wb') as fp:
					pickle.dump(highStroke, fp)
				break
			else:
				val = raw_input("Ivesk smugio jega [0 - 127] gera pradzia - 17:")
				try:
					i = int(val)
					if i >= 0 and i <= 127:
						highStroke[n] = i
						m.setHighStrokeLength(n, i)
				except ValueError:
					print("Vesk tik skaicius!")
					m.test(n)
