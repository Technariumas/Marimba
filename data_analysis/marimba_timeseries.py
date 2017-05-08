# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from note_mapping import *
from opensimplex import OpenSimplex

octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

durations = 0.5*np.divide(durations, np.max(durations))

duration = get_duration() - 1
midi = Midi(number_tracks=1, tempo=120, instrument=11)

testMidi = Midi(number_tracks=1, tempo=120, instrument=11)


sequence = -1*np.ones((10, 8, duration), dtype=int)
timeseries = -1*np.ones((4, duration), dtype=int)


for i, region in enumerate([1, 2, 3, 4]):
	mb = mb_per_second_in_region(region)
	timeseries[i,:] = make_threshold(np.rint(mb)).astype(int)


def get_Perlin_noise():
	noise_array = np.empty((sequence.shape))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array.astype(int)

for frame in range(duration):
	#tmp = OpenSimplex(seed=frame)
	#loudness_array = get_Perlin_noise()
	time_slice = timeseries[:, frame]
	for i, octave in enumerate(time_slice):
		current_boxes = get_boxes(notes[i], octave)
		sequence[current_boxes[0], current_boxes[1], frame] = index_array[current_boxes[0], current_boxes[1]]
		
		

for i, box in np.ndenumerate(index_array):
	noteSeq = []
	testNoteSeq = []
	note_sequence = sequence[i]
	for i, sound in enumerate(note_sequence):
			dur = np.random.choice(durations)
			if (sound == -1):
				noteSeq.append(Rest(0.5))
				testNoteSeq.append(Rest(0.5))
			elif note_sequence[i-1] <> -1:
				sound = -1
				noteSeq.append(Rest(0.5))
				testNoteSeq.append(Rest(0.5))
			else:
				loudness = np.random.choice([127, 127, 60, 60, 60])		
				noteSeq.append(Rest(0.5-dur))
				noteSeq.append(Note(sound, 0, dur, loudness))
				testNote, testOctave = get_real_note_from_index(sound)
				testNoteSeq.append(Rest(0.5-dur))
				testNoteSeq.append(Note(testNote, testOctave, dur, loudness))
	midi.seq_notes(noteSeq, time=0)
	testMidi.seq_notes(testNoteSeq, time=0)
midi.write("midi_output/regions_80.mid")
testMidi.write("midi_output/test_regions_80.mid")
