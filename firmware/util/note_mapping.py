# -*- coding: utf-8 -*-
import numpy as np

geom = np.genfromtxt("/home/pi/Marimba/firmware/util/notes_spatial.txt", dtype=str, delimiter = ";")

notes_spatial = np.zeros((10, 8), dtype=int)
octaves_spatial = np.zeros((10, 8), dtype=int)
for i, note in np.ndenumerate(geom):
	notes_spatial[i] = note[0]
	octaves_spatial[i] = note[1]

index_array = np.arange(80)#range(0, 80)*np.ones((10, 8))
index_array = np.reshape(index_array, (8, 10)).T

def get_switch_values():
	switch_list = []
	for i, val in np.ndenumerate(index_array):
		a = bin(val)[2:].zfill(10)
		a = a[::-1]
		b = ""
		for i, n in enumerate(a):
			if n <> "0":
				b = b+str(i+1)
		switch_list.append(b)
	switch_array = np.reshape(switch_list, (10, 8))	
	np.savetxt("conf/switches.txt", switch_array, fmt='%10s')


def get_column(array, col):
	return array[:,col]


def get_row(array, row):
	return array[row,:]

def get_boxes(tone, octave):
	return np.where((notes_spatial == tone) & (octaves_spatial == octave)) 

def get_note(tone):
	return np.where((notes_spatial == tone)) 

def get_octave(octave):
	return np.where((octaves_spatial == octave)) 

def get_real_note_from_index(ind):
	index = np.where(index_array == ind)
	octave = octaves_spatial[index]
	note = notes_spatial[index]
	return note[0], octave[0]


#print get_note(4)
#print get_boxes(7, 6)	
