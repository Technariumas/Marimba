# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from note_mapping import *
from opensimplex import OpenSimplex
from power_supply_spatial import *
import sys

octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

midi = Midi(number_tracks=1, tempo=120, instrument=11)
noteSeq = []

#for t in range(0, 80):
#	noteSeq.append(Note(t, 0, 0.125, 127))

for i, region in enumerate([1, 2, 3, 4]): #iterating over 4 notes
			for j, octave in enumerate(octaves): #iterating over 4*4 frames (setting octave values)
				noteSeq = []
				for frame in range(60): 
					current_box = get_boxes(notes[i], octave)
					playing = index_array[current_box]
					print "time:", frame, playing, "current_box", current_box
					for box in playing:
						noteSeq.append(Note(box, 0, 0.25, 60))
				print noteSeq
				midi.seq_notes(noteSeq, time=0)
midi.write("midi_output/test_pyknon.mid")


