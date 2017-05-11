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

outputName = sys.argv[1]
octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

durations = get_session_duration()
durations = 0.25*np.divide(durations, np.max(durations))
#print durations, np.max(durations)
duration = get_duration() - 1

print duration, 'track duration'

midi = Midi(number_tracks=1, tempo=120, instrument=11)
testMidi = Midi(number_tracks=1, tempo=120, instrument=11)

sequence = -1*np.ones((10, 8, duration), dtype=int)
loudness = np.zeros((10, 8, duration), dtype=int)

def get_Perlin_noise():
	noise_array = np.empty((sequence.shape))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array.astype(int)

def check_time_contiguity(timestamps, time_slice_start, time_slice_end, mb, sessions):
		time_slices_list = [datetime.strptime(time_slice_start, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=seconds) for seconds in range(1, duration+1)]
		for i, moment in enumerate(time_slices_list): #time slices -- contiguous seconds from slice_start to slice_end
			if (moment <> timestamps[i]):
				timestamps.insert(i, moment)
				mb.insert(i, 0)
				sessions.insert(i, 0)
		return timestamps, mb, sessions

def get_volume(sessions):
	sessions = np.asarray(sessions)
	mean_sessions = np.mean(sessions)
	sessions[np.where(sessions >= mean_sessions)] = 127
	sessions[np.where((sessions < mean_sessions) & (sessions <> 0))] = 60
	return sessions
	
def render_timeseries_sequence():
	timeseries = -1*np.ones((4, duration), dtype=int)
	volumeseries = np.zeros((4, duration), dtype=int) #array storing volume of each region (volume depends on session count)
	for i, region in enumerate([1, 2, 3, 4]): #iterating over 4 notes
		timestamps = get_unique_times_start(region)
		mb = mb_per_second_in_region(region)
		sessions = get_session_count(region)
		timestamps, mb, sessions = check_time_contiguity(timestamps, time_slice_start, time_slice_end, mb, sessions)
		timeseries[i,:] = make_threshold(np.rint(mb)).astype(int)
		volumeseries[i,:] = get_volume(sessions)
		for frame in range(duration): 
			time_slice = timeseries[:, frame]#octave value array sliced in time
			for j, octave in enumerate(time_slice): #iterating over 4*4 frames (setting octave values)
				current_boxes = get_boxes(notes[i], octave) #indices of boxes with a given note and octave value
				sequence[current_boxes[0], current_boxes[1], frame] = index_array[current_boxes[0], current_boxes[1]] #sequence array elements that are playing at a given time slice are filled with box numbers
				loudness[current_boxes[0], current_boxes[1], frame] = volumeseries[i,frame]
	return sequence, loudness

		
def play_timeseries(sequence, loudness):
	for i, box in np.ndenumerate(index_array):
		noteSeq = []
		testNoteSeq = []
		note_sequence = sequence[i]
		volume_sequence = loudness[i]
		for j, sound in enumerate(note_sequence):
				dur = np.random.choice([0.5, 0.5, 1, 0.25])
				if (sound == -1):
					print "quiet"
					noteSeq.append(Rest(0.5))
					#testNoteSeq.append(Rest(0.5))
				elif note_sequence[j-1] <> -1:
					sound = -1
					noteSeq.append(Rest(1))
					#testNoteSeq.append(Rest(0.5))
				else:
					noteSeq.append(Note(sound, 0, dur, volume_sequence[j]))
					noteSeq.append(Rest(1-dur))
					#testNoteSeq.append(Rest(0.5-dur))
					#testNote, testOctave = get_real_note_from_index(sound)
					#testNoteSeq.append(Note(testNote, testOctave, dur, volume_sequence[j]))
		midi.seq_notes(noteSeq, time=0)
		#testMidi.seq_notes(testNoteSeq, time=0)
	midi.write("midi_output/"+outputName+".mid")
	#testMidi.write("midi_output/test"+outputName+".mid")

#print sequence[np.where((sequence == -1) & (loudness <> 0))]

def test_power_supply_safety(loudness):
	for frame in range(duration):
		for group in range(1, 11): #iterating over all groups
			group_indices = return_current_power_supply_group_indices(group)
			if np.sum(loudness[:,:, frame][group_indices]) >= 127*4:
				loudness[:,:, frame][group_indices] = np.clip(loudness[:,:, frame][group_indices], 0, 60) 
	return loudness			

sequence, loudness = render_timeseries_sequence()
loudness = test_power_supply_safety(loudness)
play_timeseries(sequence, loudness)

'''
vo = 60*np.ones((5, 6), dtype=int)
v = 127*np.ones((5, 6), dtype=int)
vol = np.clip(np.triu(vo) + np.tril(v), 60, 127)
volume = np.append(np.fliplr(vol), vol, axis=1)
'''
