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

for i, region in enumerate([1, 2, 3, 4]):
	mb = mb_per_second_in_region(region)
	ts = make_threshold(np.rint(mb)) #
	ind = 0
	for j, octave in enumerate(octaves):
		octave_series[j, :][np.where(ts == octave)] = octave#(region, octave, 0.5, 127)
		note_series[j, :][np.where(ts == octave)] = notes[i]
		ind+=1

print octave_series


'''
def make_sequence(noteSeq, row):
	for el in row:
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
	return noteSeq	'''


for box in range(0, 16):
	noteSeq = []
	for frame in range(duration):
			#sekos trukme
			noteSeq.append(Note(note_series[frame], octave_series[frame], 0.125, 60))
			noteSeq.append(Rest(0.125))
			noteSeq.append(Rest(0.125))
			noteSeq.append(Rest(0.125))
	midi.seq_notes(noteSeq, time=0)
midi.write("midi_output/regions.mid")

exit()

plt.figure()
for region in [1, 2, 3, 4]:
	ax = plt.subplot(2, 2, region)
	mb = get_mb_in_region(region)
	session_start = get_time_start_in_region(region)
	arr = np.column_stack([session_start, mb])
	df = pd.DataFrame(arr, columns=['time', 'mb'])
	#np.column_stack([session_start, mb]), index=['time', 'mb'])
	#avg = pd.rolling_median(df, window, center=True)
	ax.plot(df['time'], df['mb'])
	avg = pd.rolling_mean(df['mb'], window_size, center=True)
	ax.plot(df['time'], avg)
	#ax.plot_date(session_start, mb, c='k', markersize=1)
	#ax.plot(session_start, avg, c='r', linestyle='-', markersize=1)
	#plt.date_plot(districts, mb)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%S'))
	ax.set_yscale('log')
plt.ylabel("MB, vidurkis")
plt.savefig("img/test_avg", bbox_inches="tight")
