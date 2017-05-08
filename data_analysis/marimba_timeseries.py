# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest

octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

durations = 0.5*np.divide(durations, np.max(durations))
#durations*= 0.125
#print durations


def make_threshold(array):
	lowest = np.percentile(array, 25)
	lower = np.percentile(array, 50)
	upper = np.percentile(array, 75)
	lowest_octave = np.where(array <= lowest)
	lower_octave = np.where((array <= lower) & (array > lowest))
	upper_octave = np.where((array <= upper) & (array > lower))
	top_octave = np.where(array > upper)
	array[lowest_octave] = 3
	array[lower_octave] = 4
	array[upper_octave] = 5
	array[top_octave] = 6		
	return array

duration = get_duration() - 1
sequence = np.zeros((16, duration), dtype=[('value', 'i2'), ('octave', 'i2'), ('dur', 'f4'), ('vol', 'i4')])
midi = Midi(number_tracks=1, tempo=120, instrument=11)

octave_series = np.zeros((16, duration))
note_series = octave_series.copy()

ind = 0
for i, region in enumerate([1, 2, 3, 4]):
	mb = mb_per_second_in_region(region)
	ts = make_threshold(np.rint(mb)) #
	for j, octave in enumerate(octaves):
		octave_series[ind, :][np.where(ts == octave)] = octave#(region, octave, 0.5, 127)
		note_series[ind, :][np.where(ts == octave)] = notes[i]
		ind+=1

'''
def make_sequence(noteSeq, row):
	for el in row:
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
	return noteSeq	'''


for box in range(16):
	noteSeq = []
	for frame in range(duration):
			#sekos trukme
			dur = np.random.choice(durations)
			#dur = 0.125
			el = Note(note_series[box,frame], octave_series[box,frame], dur, 127)
			#noteSeq.append(el)
			#noteSeq.append(el)
			#noteSeq.append(el)
			noteSeq.append(el)
			noteSeq.append(Rest(0.5 - dur))
			#noteSeq.append(Rest(0.125))
			#noteSeq.append(Rest(0.125))
	midi.seq_notes(noteSeq, time=1)
midi.write("midi_output/regions.mid")

exit()

plt.figure()
for region in [1, 2, 3, 4]:
	ax = plt.subplot(2, 2, region)
	mb = mb_per_second_in_region(region)#make_threshold(np.rint(mb))
	ax.plot(mb)
	#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%S'))
	#ax.set_yscale('log')
plt.ylabel("MB, vidurkis")
plt.savefig("img/mb_per_second_regions", bbox_inches="tight")
