# -*- coding: utf-8 -*-
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest
from utils import *
from opensimplex import OpenSimplex
from datetime import datetime, timedelta
from marimba_config import *

octaves = [1, 2, 3, 4]
note_values = ["C", "D", "F", "G"]

def make_sequence(noteSeq, row):
	for el in row:
		print el, 'el'
		noteSeq.append(Note(el[0], el[1], el[2], el[3]))
	return noteSeq	


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
	
duration = 120 #In 1/16ths. 30 seconds, 60 quarter notes, 120 1/8th notes, 240 1/16th notes
midi = Midi(number_tracks=1, tempo=120)

#fig = plt.figure()


sequence = np.zeros((16, duration), dtype=[('value', 'i2'), ('octave', 'i2'), ('dur', 'f4'), ('vol', 'i4')])

for frame in range(0, duration):
	tmp = OpenSimplex(seed=frame)
	loudness = get_Perlin_noise()
	cnt = 0
	while cnt < 16:
		for i, note in enumerate([0, 2, 5, 7]):
			for j, octave in enumerate([3, 4, 5, 6]):
				print i, j, cnt, frame, "i, j, i*j, frame"
				print 'note, octave, loudness', note, octave, loudness[i, j]
				sequence[cnt, frame] = (note, octave, 0.125, loudness[i, j])
				cnt += 1
print sequence, sequence.shape
	#c = plt.imshow(noise, interpolation=None, cmap='viridis')
	#plt.colorbar(c)
#plt.show()	
	

midi = Midi(number_tracks=16, tempo=120)

for row in sequence:
		noteSeq = []
		noteSeq = make_sequence(noteSeq, row)
		midi.seq_notes(noteSeq, time=0)
		

midi.write("midi_output/test.mid")

'''
for i, region in enumerate(regions):
	mb = get_mb_in_region(region)
	avg = rolling_sum(mb, 60)
	note = region_notes[i]
	notes1 = NoteSeq([Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127), Note(note, octave=5, dur=0.25, volume=127)])
	midi.seq_notes(notes1, track=i)
'''

