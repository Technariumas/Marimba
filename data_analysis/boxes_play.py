# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from opensimplex import OpenSimplex

regions = [1, 2, 3, 4]
octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

durations = np.divide(durations, np.max(durations))
duration = get_duration() - 1

midi = Midi(number_tracks=1, tempo=120, instrument=11)

sequence = np.zeros((80, duration), dtype=[('value', 'i2'), ('octave', 'i2'), ('dur', 'f4'), ('vol', 'i4')])

def get_Perlin_noise():
	noise_array = np.empty((4, 4))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	#print np.min(noise_array), np.mean(noise_array), np.max(noise_array)	
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array

def make_sequence(noteSeq, row):
	for el in row:
		noteSeq.append(Rest(0.5))
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
		noteSeq.append(Rest(0.5))
	return noteSeq	

for frame in range(0, duration):
	tmp = OpenSimplex(seed=frame)
	loudness = get_Perlin_noise()
	cnt = 0
	while cnt < 80:
		for i, note in enumerate([0, 2, 5, 7]):
			for j, octave in enumerate([3, 4, 5, 6]):
				for k, loudness in enumerate(np.random.choice([127, 60, 60, 0, 0], 5)):
					dur = np.random.choice(durations)
					print i, j, k, cnt, loudness, frame, "i, j, cnt, loudness, frame"
					#print 'note, octave, loudness', note, octave, loudness[i, j]
					sequence[cnt, frame] = (cnt, 0, dur, loudness)
					cnt += 1

#sequence = sequence[0:3,:]

	
for row in sequence:
		noteSeq = []
		noteSeq = make_sequence(noteSeq, row)
		midi.seq_notes(noteSeq, time=0)

midi.write("midi_output/test_80.mid")

exit()
octave_series = np.ones((16, duration), dtype="int")
note_series = octave_series.copy()

ind = 0
for i, region in enumerate([1, 2, 3, 4]): #iterating over notes
	mb = mb_per_second_in_region(region)
	ts = make_threshold(np.rint(mb)) 
	for j, octave in enumerate(octaves): #iterating over octaves 
		octave_series[ind, :][np.where(ts == octave)] = octave#(region, octave, 0.5, 127)
		note_series[ind, :][np.where(ts == octave)] = notes[i]
		ind+=1

print note_series

geom = np.genfromtxt("conf/notes_spatial.txt", dtype=(('str')), delimiter = ";")

notes_spatial = np.zeros((10, 8))
octaves_spatial = np.zeros((10, 8))
volume_arr = 127*np.ones((10, 8))

for i, note in np.ndenumerate(geom):
	notes_spatial[i] = note[0]
	octaves_spatial[i] = note[1]


noteSeq = []
midi = Midi(number_tracks=1, tempo=120, instrument=11)
noteSeq.append(Note(0, 0, 0.5, 127))
noteSeq.append(Note(77, 0, 0.5, 127))

midi.seq_notes(noteSeq, time=0)
midi.write("midi_output/regions_80.mid")
