import pygame
import os

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

def play_sound(note, volume):
	print(note)
	sound = midi_filenames[note]
	sound.set_volume(1/127*volume)
	sound.play()
	sound.fadeout(1000)