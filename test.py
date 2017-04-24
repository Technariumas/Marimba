import random
from player import Player



sequences = [[(36,70,15),(72,70,0.5)],[(36,70,1),(72,70,1)],
		[(36,70,1),(72,70,2)],[(60,70,1),(77,70,1)],[(60,70,1)],
		[],[],[],[(62,70,1),(67,70,1)],[(79,70,1),(77,70,1)]]

Player.init() # call player init before playing anything
Player.play_all(sequences) 
Player.to_midi(sequences, 120, 'test.mid') # use to_midi to write sequence to a midi file
