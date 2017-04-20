import pygame
import os
import asyncio
from midiutil.MidiFile3 import MIDIFile 

def init():
	global midi_filenames
	pygame.init()
	pygame.mixer.init()
	screen=pygame.display.set_mode((1,1),0,32)
	cwd =  os.path.dirname(os.path.realpath(__file__))
	files_dir = os.path.join(cwd, 'files')

	# map midi note codes to note names
	midi_filenames = {
	36:'C3',
	38: 'D3',
	41: 'F3',
	43: 'G3',
	48: 'C4',
	50: 'D4',
	53: 'F4',
	55: 'G4',
	60: 'C5',
	62: 'D5',
	65: 'F5',
	67: 'G5',
	72: 'C6',
	74: 'D6',
	77: 'F6',
	79: 'G6',
	}

	# map note codes to file names
	midi_filenames = {key: midi_filenames[key]+'.wav' for key in midi_filenames}

	# map note codes to sound objects
	midi_filenames = {key: pygame.mixer.Sound(os.path.join(files_dir, midi_filenames[key])) for key in midi_filenames}



async def play_note(start_time, delay, note, velocity,  lenght=1):
	'''start_time in beats'''
	await asyncio.sleep(start_time*delay) # wait for the time to start
	sound = midi_filenames[note]
	sound.set_volume(1/127*velocity)
	sound.play()
	await asyncio.sleep(delay*lenght) # wait for the lenght of note before fadeout
	sound.fadeout(1) 

def play_all(sequence, bpm = 120):

	delay = 60/bpm # this is time between beats in seconds 
	ioloop = asyncio.get_event_loop()
	tasks = []
	for index, notes in enumerate(sequence):
		if notes:
			for note in notes:
				tasks.append(ioloop.create_task(play_note(index, delay, *note)))
	ioloop.run_until_complete(asyncio.wait(tasks))


def to_midi(sequence, bpm, filename):
	track = 0
	channel = 0
	midi = MIDIFile(1)
	midi.addTempo(track, channel, bpm)
	start_time = 0
	for notes in sequence:
		if notes:
			for note in notes:
				midi.addNote(track, channel, note[0], start_time, note[2], note[1])
		start_time+=1
	output_file = open(filename, "wb")
	midi.writeFile(output_file)
