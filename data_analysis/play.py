# -*- coding: utf-8 -*-
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from utils import *
from opensimplex import OpenSimplex
from datetime import datetime, timedelta
from marimba_config import *
from power_supply_spatial import *
import sys

outputName = sys.argv[1]

octaves = [1, 2, 3, 4]
note_values = ["C", "D", "F", "G"]
#durations = 0.25*np.divide(durations, np.max(durations))

def make_sequence(noteSeq, row):
	for el in row:
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
	return noteSeq	

def make_threshold(noise_array):
	lower_third = np.percentile(noise_array, 50)
	upper_third = np.percentile(noise_array, 80)
	noise_array = np.clip(noise_array, lower_third, upper_third)
	noise_array[np.where(noise_array == lower_third)] = 0
	noise_array[np.where(noise_array == upper_third)] = 127
	noise_array[np.where((noise_array <> 0) & (noise_array <> 127))] = 60
	return np.rint(noise_array)
	
def get_Perlin_noise(shape):
	noise_array = np.zeros((shape))	
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	#print np.min(noise_array), np.mean(noise_array), np.max(noise_array)	
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array
	
def test_power_supply_safety(loudness):
	for frame in range(duration):
		for group in range(1, 11): #iterating over all groups
			group_indices = return_current_power_supply_group_indices(group)
			if np.sum(loudness[:,:, frame][group_indices]) >= 127*4:
				loudness[:,:, frame][group_indices] = np.clip(loudness[:,:, frame][group_indices], 0, 60) 
	return loudness		

		
def play_timeseries(sequence):
	index_array = np.arange(80)#range(0, 80)*np.ones((10, 8))
	index_array = np.reshape(index_array, (8, 10)).T
	for i, box in np.ndenumerate(index_array):
		noteSeq = []
		note_sequence = sequence[i] 
		for j, sound in enumerate(note_sequence):
			if note_sequence[j-1] <> 0:
				sound = -1
				noteSeq.append(Rest(0.5))
			else:
				print "play", box, note_sequence[j]
				noteSeq.append(Note(box, 0, 0.25, note_sequence[j]))
		midi.seq_notes(noteSeq, time=0)
	midi.write("midi_output/"+outputName+".mid")

	
duration = 60

midi = Midi(number_tracks=1, tempo=60, instrument=11)

sequence = -1*np.ones((10, 8, duration), dtype=int)

for moment in range(0, duration):
	frame = sequence[:, :, moment]
	tmp = OpenSimplex(seed=moment)
	sequence[:, :, moment] = get_Perlin_noise(frame.shape)

sequence = test_power_supply_safety(sequence)

play_timeseries(sequence)

print sequence
exit()

'''for row in sequence:
		print row, len(row), "length"
		noteSeq = []
		noteSeq = make_sequence(noteSeq, row)
		midi.seq_notes(noteSeq, time=0)
		
midi.write("midi_output/test.mid")
'''
exit()

'''
for i, region in enumerate(regions):
	mb = get_mb_in_region(region)
	avg = rolling_sum(mb, 60)
	note = region_notes[i]
	notes1 = NoteSeq([Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127)])
	midi.seq_notes(notes1, track=i)
'''

