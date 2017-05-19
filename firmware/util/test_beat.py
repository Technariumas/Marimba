import sys
from marimba import Marimba
import time

m = Marimba()
m.connect()

#volume = int(sys.argv[1])
box = int(sys.argv[1])
duration = int(sys.argv[2])
length = int(sys.argv[3])

print "playing box #", box
while True:
	sequence = [box for box in range(0, length)]
	print sequence
	m.playSequence(sequence, 0, duration)
	sleep(10)
#notes, delay, duration
