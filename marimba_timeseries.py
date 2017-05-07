# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
window_size = 60


def make_threshold(array):
	lowest = np.percentile(array, 25)
	lower = np.percentile(array, 50)
	upper = np.percentile(array, 75)
	lowest_octave = np.where(array <= lowest)
	lower_octave = np.where((array <= lower) & (array > lowest))
	upper_octave = np.where((array <= upper) & (array > lower))
	top_octave = np.where(array > upper)
	print lowest_octave, lowest
	array[lowest_octave] = 3
	array[lower_octave] = 4
	array[upper_octave] = 5
	array[top_octave] = 6		
	return array

duration = 60
sequence = np.zeros((0, duration), dtype=[('value', 'i2'), ('octave', 'i2'), ('dur', 'f4'), ('vol', 'i4')])

midi = Midi(number_tracks=1, tempo=120, instrument=11)
timeseries = np.zeros((4, duration))

for i, region in enumerate([1, 2, 3, 4]):
	mb = np.asarray(get_mb_in_region(region))
	ts = np.sum(rolling_window(mb, window_size), -1)#make_threshold(np.rint(pd.rolling_mean(df['mb'], window, center=True)))
	print ts.shape
	timeseries[i, :] = np.concatenate((ts, ts[0:window_size-1]))
	print timeseries



for row in sequence:
		noteSeq = []
		seq = pd.rolling_mean(df['mb'], window, center=True)
		print seq, 'mean'
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
		midi.seq_notes(noteSeq, time=0)
midi.write("midi_output/regions.mid")

exit()

plt.figure()
for region in [1, 2, 3, 4]:
	ax = plt.subplot(2, 2, region)
	mb = get_mb_in_region(region)
	session_start = get_time_start_in_region(region)
	#arr = np.column_stack([session_start, mb])
	df = pd.DataFrame(np.column_stack([session_start, mb]), columns=['time', 'mb'])
	#np.column_stack([session_start, mb]), index=['time', 'mb'])
	#avg = pd.rolling_median(df, window, center=True)
	ax.plot(df['time'], df['mb'])
	ax.plot(df['time'], pd.rolling_mean(df['mb'], window, center=True))
	#ax.plot_date(session_start, mb, c='k', markersize=1)
	#ax.plot(session_start, avg, c='r', linestyle='-', markersize=1)
	#plt.date_plot(districts, mb)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%S'))
	ax.set_yscale('log')
plt.ylabel("MB, vidurkis")
plt.savefig("img/test_avg", bbox_inches="tight")
