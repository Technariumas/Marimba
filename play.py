# -*- coding: utf-8 -*-
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from utils import *
from opensimplex import OpenSimplex
from datetime import datetime, timedelta
from marimba_config import *


regions = [1, 2, 3, 4]
region_notes = ["C", "D", "F", "G"]

tmp = OpenSimplex()

def get_Perlin_noise():
	noise_array = np.empty((10, 8))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = tmp.noise2d(i[0], i[1])
	return noise_array
	
print get_Perlin_noise()

#seq1 = NoteSeq([Note(x) for x in range(0, 12, 1)])#NoteSeq("C4 D8 R E")
#seq2 = NoteSeq("F G A")
seq1 = NoteSeq([Note(0, 5, 0.25, 127), Rest(0.5), Note(5, 3, 0.5, 127)])
midi = Midi(number_tracks=16, tempo=120)
midi.seq_notes(seq1, time=0)
#midi.seq_notes(seq2, time=4)


'''
for i, region in enumerate(regions):
	mb = get_mb_in_region(region)
	avg = rolling_sum(mb, 60)
	note = region_notes[i]
	notes1 = NoteSeq([Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127)])
	midi.seq_notes(notes1, track=i)
'''
midi.write("midi_output/test.mid")
