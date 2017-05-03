# -*- coding: utf-8 -*-
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from utils import *
from opensimplex import OpenSimplex
from datetime import datetime, timedelta
from marimba_config import *

octaves = [1, 2, 3, 4]
note_values = ["C", "D", "F", "G"]


def make_threshold(noise_array):
	lower_third = np.percentile(noise_array, 33)
	upper_third = np.percentile(noise_array, 66)
	noise_array = np.clip(noise_array, lower_third, upper_third)
	noise_array[np.where(noise_array == lower_third)] = 0
	noise_array[np.where(noise_array == upper_third)] = 127
	return np.rint(noise_array)
	
def get_Perlin_noise():
	noise_array = np.empty((4, 4))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	print np.min(noise_array)	
	#print np.min(noise_array), np.mean(noise_array), np.max(noise_array)	
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array
	
duration = 10 #30 seconds, 60 quarter notes, 120 1/8th notes, 240 1/16th notes
midi = Midi(number_tracks=16, tempo=120)

#fig = plt.figure()

seq1 = NoteSeq([])
seq2 = NoteSeq([])
seq3 = NoteSeq([])
seq4 = NoteSeq([])
seq5 = NoteSeq([])
seq6 = NoteSeq([])
seq7 = NoteSeq([])
seq8 = NoteSeq([])


sequence = np.zeros((16, duration))

for i in range(0, duration):
	tmp = OpenSimplex(seed=i)
	loudness = get_Perlin_noise()
	for i, note in enumerate(["C", "D", "F", "G"]):
		for j, octave in enumerate([3, 4, 5, 6]):
			#print note, octave, loudness[i, j]
			print loudness[i, j], 'loudness'
			seq1.append(Note(0, 3, 0.125, loudness[i, j]))
			seq2.append(Note(2, 4, 0.125, loudness[i, j]))
			seq3.append(Note(5, 5, 0.125, loudness[i, j]))
			seq4.append(Note(7, 6, 0.125, loudness[i, j]))
			seq5.append(Note(0, 4, 0.125, loudness[i, j]))
			seq6.append(Note(2, 3, 0.125, loudness[i, j]))
			seq7.append(Note(5, 6, 0.125, loudness[i, j]))
			seq8.append(Note(7, 5, 0.125, loudness[i, j]))


	#c = plt.imshow(noise, interpolation=None, cmap='viridis')
	#plt.colorbar(c)
#plt.show()	
	
	
#seq1 = NoteSeq([Note(x) for x in range(0, 12, 1)])#NoteSeq("C4 D8 R E")
#seq2 = NoteSeq("F G A")
#seq1 = NoteSeq([Note(0, 5, 0.25, 127), Rest(0.5), Note(5, 3, 0.5, 127)])
midi = Midi(number_tracks=16, tempo=120)
midi.seq_notes(seq1, time=0)
midi.seq_notes(seq2, time=1)
midi.seq_notes(seq3, time=2)
midi.seq_notes(seq4, time=4)
midi.seq_notes(seq5, time=5)
midi.seq_notes(seq6, time=6)
midi.seq_notes(seq7, time=7)
midi.seq_notes(seq8, time=8)
midi.write("midi_output/test.mid")

'''
for i, region in enumerate(regions):
	mb = get_mb_in_region(region)
	avg = rolling_sum(mb, 60)
	note = region_notes[i]
	notes1 = NoteSeq([Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127)])
	midi.seq_notes(notes1, track=i)
'''

