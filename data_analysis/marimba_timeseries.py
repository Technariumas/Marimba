from __future__ import division
import matplotlib.pyplot as plt
import random

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from note_mapping import *
from opensimplex import OpenSimplex
from power_supply_spatial import *
import sys


CHANNEL_PARAM_LED_STEP = 1
CHANNEL_PARAM_LED_MINIMUM = 2
CHANNEL_PARAM_LED_MAXIMUM = 3

outputName = sys.argv[1]
octaves = [3, 4, 5, 6]
note_values = ["C", "D", "F", "G"]
notes = [0, 2, 5, 7]

#durations = get_session_duration()
duration = get_duration() - 1
midi = Midi(number_tracks=4, channel = [0, CHANNEL_PARAM_LED_STEP, CHANNEL_PARAM_LED_MINIMUM, CHANNEL_PARAM_LED_MAXIMUM], tempo=120, instrument=11)
#testMidi = Midi(number_tracks=1, tempo=120, instrument=11)

sequence = -1*np.ones((10, 8, duration), dtype=int)
loudness = np.zeros((10, 8, duration), dtype=int)
'''
def get_Perlin_noise():
	noise_array = np.empty((sequence.shape))
	for i, x in np.ndenumerate(noise_array):
		noise_array[i] = 1 + tmp.noise2d(i[0], i[1])
	noise_array = make_threshold(60*noise_array)#midpoint between 0 and 127
	return noise_array.astype(int)
'''
def check_time_contiguity(timestamps, time_slice_start, time_slice_end, mb, sessions):
		time_slices_list = [datetime.strptime(time_slice_start, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=seconds) for seconds in range(1, duration+1)]
		for i, moment in enumerate(time_slices_list): #time slices -- contiguous seconds from slice_start to slice_end
			if (moment <> timestamps[i]):
				print moment, timestamps[i], "time"
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
		print region, "changing region"
		mb = mb_per_second_in_region(region)
		sessions = get_session_count(region)
		timestamps, mb, sessions = check_time_contiguity(timestamps, time_slice_start, time_slice_end, mb, sessions)
		timeseries[i,:] = make_threshold(np.rint(mb), notes[i]).astype(int)
		volumeseries[i,:] = get_volume(sessions)
		for frame in range(duration):
			time_slice = timeseries[i, frame]#octave value array sliced in time
			#for j, octave in enumerate(time_slice): #iterating over 4*4 frames (setting octave values)
			if time_slice <> -1:
					current_boxes = get_boxes(notes[i], time_slice) #indices of boxes with a given note and octave value
					sequence[current_boxes[0], current_boxes[1], frame] = index_array[current_boxes[0], current_boxes[1]] #sequence array elements that are playing at a given time slice are filled with box numbers
					loudness[current_boxes[0], current_boxes[1], frame] = volumeseries[i,frame]
					#print "note", notes[i], "octave", time_slice, current_boxes[0], current_boxes[1], "boxes"
					#print "notes, octaves", i, j
		print "time: ", frame			
	return sequence, loudness


def get_lowest_notes():
	box_list = []
	for tone in [7]:
		for octave in [3]:
			boxes = index_array[get_boxes(tone, octave)]
			box_list.append(boxes.tolist())
	return box_list

highest_notes = [21, 45,  12, 1, 24, 32, 7, 69, 20, 43, 70, 2]

#print get_lowest_notes()

lowest_notes = [61, 73, 54, 65, 39, 60, 71, 35, 16, 58, 0, 50, 11, 23, 36, 53, 44, 46, 67, 49, 62, 14, 76, 27, 68, 10, 31, 51, 63, 75, 30, 52, 3, 37, 18, 40, 33, 5, 26, 59]

rhythm_notes = lowest_notes+highest_notes

lowest_octave = [61, 73, 54, 65, 39, 60, 71, 35, 16, 58, 0, 50, 11, 23, 36, 53, 44, 46, 67, 49]
lowest_F = [0, 50, 11, 23, 36]
lowest_G = [53, 44, 46, 67, 49]

def flash_lights(note):
	current_max_brightness = 127
	seq = []
	for i in range(0, 30):
		current_max_brightness-=4
		seq.append(Note(note, 0, 0.1, current_max_brightness))
		seq.append(Rest(0.1))
		print current_max_brightness, "dimming"
	for i in range(0, 30):
		current_max_brightness+=4 
		seq.append(Note(note, 0, 0.1, current_max_brightness)) 
		seq.append(Rest(0.1))
		print current_max_brightness, "brightening"
	return seq


def play_timeseries(sequence, loudness):
	frame_counter = np.zeros((duration))
	current_max_brightness = 127
	lightStepSeq = []
	lightMaxSeq = []
	lightMinSeq = []
	for box in range(80):
		lightStepSeq.append(Note(box, 0, 0.125, 3))
		lightStepSeq.append(Rest(0.125))
		lightMinSeq.append(Note(box, 0, 0.125, 15))
		lightMinSeq.append(Rest(0.125))
		lightMaxSeq.append(Note(box, 0, 0.125, 127))
		lightMaxSeq.append(Rest(0.125))
	'''
	for time in range(duration):
		if time % 60 == 0:
			for i in range(0, 30):
				current_max_brightness-=4
				lightStepSeq.append(Note(14, 0, 0.25, current_max_brightness))
				lightStepSeq.append(Rest(0.25))
				print current_max_brightness, "dimming"
			for i in range(0, 30):
				current_max_brightness+=4 
				lightStepSeq.append(Note(14, 0, 0.25, current_max_brightness)) 
				lightStepSeq.append(Rest(0.25))
				print current_max_brightness, "brightening"
	'''
	for i, box in np.ndenumerate(index_array):
		#print i, box, index_array[i]
		noteSeq = []
		note_sequence = sequence[i]
		volume_sequence = loudness[i]
		for j, sound in enumerate(note_sequence):
			if box in lowest_octave:
					dur = 2
			elif box in lowest_F:
					dur = 1.5
			elif box in lowest_G:
					dur = 1
			else:
					dur = 1#np.random.choice([1, 1])#], 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375, 0.375])
			if (sound == -1):
					noteSeq.append(Rest(1))
			elif (note_sequence[j-1] <> -1):# or (note_sequence[j-2] <> -1):
					sound = -1
					noteSeq.append(Rest(1))
			elif (j%127 == 0):
				if frame_counter[j+1] == 0:
					noteSeq.append(Rest(1))
			elif j%128 == 0:
				print "32", box
				region_notes = []
				if frame_counter[j] == 0:
					if random.randint(1,4) > 3:
						for octave in random.sample([3, 4, 5, 6], 1):
							#note = get_real_note_from_index(box)[0]
							note = random.sample([0, 2, 5, 7], 1)
							rn = index_array[get_boxes(note, octave)].tolist()
							region_notes = region_notes + rn
						if octave%2 == 0:
							region_list = region_notes[0:3]	
						else:
							region_list = region_notes[0:3][::-1]
						for rn in region_list:
							currentNote = Note(rn, 0, 0.6667/2, 60)
							noteSeq.append(currentNote)
							noteSeq.append(Rest(0.6667/2))
						note_duration = 3*((0.6667/2 + 0.6667/2))#len(region_notes)
						noteSeq.append(Rest(1-note_duration))
					frame_counter[j] = j
			else:
					if j in highest_notes:
							volume_sequence[j] = 60
					elif j in lowest_notes:
							volume_sequence[j] = 127	
					#noteSeq.append(Rest(0.5))
					pauseDur = 0#(box%5)*0.003
					
					if random.randint(1,100)> 35:#(j in highest_notes) or (j in lowest_notes):
						#noteDur = 0.125#+(box)*0.003 #500ms, 0.125 - 1/16 #384ms damperio trukme
						currentNote = Note(sound, 0, dur, volume_sequence[j])
						time_on = (j % 4)
						#print time_on, "time_on, 60 %"						
						noteSeq.append(currentNote)#volume_sequence[j]))
						noteSeq.append(Rest(1 - (dur+pauseDur)))
					else:
						if j%5 == 4:
							currentNote = Note(sound, 0, dur, volume_sequence[j])
							if box%4 <> 0:
								time_on = 4*(box % 15)*(0.16667/2)
								#print time_on, "time on -- j%2"
							else:	
								time_on = 4*(box % 6)*(0.333/2)#+0.125/2
								#print time_on, " 333, time_on"
							noteSeq.append(currentNote)#volume_sequence[j]))
							noteSeq.append(Rest(1 - (dur+pauseDur)))

		#noteSeq.insert(0, noteSeq[-1])
		#midi.seq_notes(noteSeq, time=time_on, track=0)
	print lightStepSeq	
	midi.seq_notes(lightStepSeq, time=4, track=CHANNEL_PARAM_LED_STEP)
	midi.seq_notes(lightMinSeq, time=4, track=CHANNEL_PARAM_LED_MINIMUM)
	midi.seq_notes(lightMaxSeq, time=4, track=CHANNEL_PARAM_LED_MAXIMUM)
	midi.write("midi_output/"+outputName+".mid")
	#testMidi.write("midi_output/"+outputName+".mid")

#print sequence[np.where((sequence == -1) & (loudness <> 0))]


def test_power_supply_safety(loudness):
	for frame in range(duration):
		for group in range(1, 11): #iterating over all groups
			group_indices = return_current_power_supply_group_indices(group)
			if np.sum(loudness[:,:, frame][group_indices]) >= 127*4:
				print "clipping", np.where(loudness[:,:, frame] >= 127)[0].shape
				loudness[:,:, frame][group_indices] = np.clip(loudness[:,:, frame][group_indices], 0, 60) 
	return loudness			

sequence, loudness = render_timeseries_sequence()
loudness = test_power_supply_safety(loudness)

for frame in range(duration):
	print frame, "played notes", "loudness:", np.where(loudness[:,:,frame] > 0)[0].shape, loudness[:,:,frame][np.where(loudness[:,:,frame] > 0)], np.where(sequence[:,:,frame] > -1)[0].shape
	
play_timeseries(sequence, loudness)

'''
vo = 60*np.ones((5, 6), dtype=int)
v = 127*np.ones((5, 6), dtype=int)
vol = np.clip(np.triu(vo) + np.tril(v), 60, 127)
volume = np.append(np.fliplr(vol), vol, axis=1)
'''
