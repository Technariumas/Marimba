from player import Player
import pandas as pd
import time
import asyncio
from midiutil import MIDIFile

PATTERNS =	[[0, 0, 0, 0, 0, 0, 0, 0], #0
			[1, 0, 0, 0, 0, 0, 0, 0], #1
			[1, 0, 0, 0, 1, 0, 0, 0], #2
			[1, 0, 1, 0, 1, 0, 0, 0], #3
			[1, 0, 1, 0, 1, 0, 1, 0], #4
			[1, 1, 1, 0, 1, 0, 1, 0], #5
			[1, 1, 1, 0, 1, 1, 1, 0], #6
			[1, 1, 1, 1, 1, 1, 1, 1]] #7

MAX_MB = [10,10,1,1] # max mb, these values directly impact the intensity of the patterns generated


def pattern_from_mb_interval(mb, max_mb):
	''' maps mb count to one of the patterns depending on the value'''
	pattern_index = int(mb*7/max_mb)
	try:									# if mb > max_mb value, use the last pattern
		pattern = PATTERNS[pattern_index]
	except IndexError:
		pattern = PATTERNS[7]
	return pattern

def index_to_note(index):
	'''patterns are converted into a 16 x N matrix where each column is patterns for one of the 16 notes.
	given the index of the column, this returns the midi code of the note'''
	dt = {0:36, 1:38, 2:41, 3:43,4:48,5:50,6:53,7:55,8:60,9:96,10:65,11:67,12:72,13:74,14:77,15:79}
	return dt[index]

'''DATA PROCESSING'''

def fix_empty_regions(arr):
	''' fills empty values so there would always be 4 rows for each second'''
	new_list = []
	counter = 1
	index = 0
	while True:		
		try:
			i = arr[index]
		except:
			break
		if counter == int(i[3]):
			new_list.append(i)
		else:
			new_list.append((i[0],i[1],i[2],counter, 0, 0, 0,0,0,0))
			index-=1
		if counter > 3:
			counter = 1
		else:
			counter+=1
		index+=1
	return new_list


def group_to_regions(fixed_data):
	'''groups the data into lists of 4 items'''
	pats = []
	for a, b, c, d in zip(*[iter(fixed_data)]*4):
		pat = []
		for i in [a,b,c,d]:
			pat.append(i)
		pats.append(pat)
	return pats



def get_patterns(grouped_data):
	'''convert data into patterns'''
	all_patterns = []
	for second in grouped_data:
		for row in second:
				all_patterns.append(pattern_from_mb_interval(row[6], MAX_MB[0]))
				all_patterns.append(pattern_from_mb_interval(row[7], MAX_MB[1]))
				all_patterns.append(pattern_from_mb_interval(row[8], MAX_MB[2]))
				all_patterns.append(pattern_from_mb_interval(row[9], MAX_MB[3]))
	return all_patterns

def group_patterns(all_patterns):
	'''group the patterns into 16 x N matrix'''
	counter = 0
	all_pat = []
	new_pat = []
	for pattern in all_patterns:
		new_pat.append(pattern)
		counter+=1
		if counter > 15:
			counter = 0
			all_pat.append(new_pat)
			new_pat = []
	return all_pat


'''UTILS TO PLAY SOUNDS'''
'''
async def play_pattern(pattern, tempo, note_index):

	delay = 60/tempo
	pitch = index_to_note(note_index)
	for note in pattern:
		if note == 1:
			Player.play_sound(pitch, 127, 2000)
			await asyncio.sleep(delay)	
		else:
			await asyncio.sleep(delay)

def sequencer(patterns, tempo):
	'in > list of lists of patterns, plays notes using pygame for testing'
	for sequences in patterns:
		index = 0
		ioloop = asyncio.get_event_loop()
		tasks = []
		for sequence in sequences:
			#pitch = index_to_note(index)
			tasks.append(ioloop.create_task(play_pattern(sequence, tempo, index)))
			index +=1
		ioloop.run_until_complete(asyncio.wait(tasks))
	ioloop.close()
'''

'''MIDI UTILS'''

def pattern_to_midi(pattern, file, note, start_time, duration = 1, volume=127):
	'''writes one pattern to midi'''
	track = 0
	channel = 0
	for ping in pattern:
		if ping != 0:
			file.addNote(track, channel, note, start_time, duration,volume)
		start_time+=1

def patterns_to_midi(patterns, file, start_time):
	'''writes 16 patterns to midi, each pattern is for a different note'''
	note_index = 0
	for pattern in patterns:
		note = index_to_note(note_index)
		pattern_to_midi(pattern, file, note, start_time)
		note_index +=1

def grouped_patterns_to_midi(grouped_patterns, file):
	'''takes grouped patterns and writes them to midi'''
	start_time = 0
	counter = 0
	lenght = len(grouped_patterns)

	for patterns in grouped_patterns:
		print('processed '+ str(counter) + ' patterns out of '+ str(lenght))
		counter+=1
		patterns_to_midi(patterns, file, start_time)
		start_time += 8


data = pd.read_csv('aggregated_data_snippet.csv') # this takes data aggregated into regions from agg_csv_to_csv.py 
fixed_data = 		fix_empty_regions(data.to_records())
grouped_data = 		group_to_regions(fixed_data)
patterns = 			get_patterns(grouped_data)
grouped_patterns = 	group_patterns(patterns)

midi = MIDIFile(1)
midi.addTempo(0, 0, 120)

grouped_patterns_to_midi(grouped_patterns[1000:3000], midi) # python hangs if trying to write the whole file
print('Done processing, writing to file')

output_file = open("test.mid", "wb")
midi.writeFile(output_file)
output_file.close()