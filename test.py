import random
import time
from player import Player


for i in range(12):
	note=random.choice(list(Player.midi_filenames.keys()))
	volume = random.randint(50,127)
	print(note)
	Player.play_sound(note, volume)
	time.sleep(0.2)