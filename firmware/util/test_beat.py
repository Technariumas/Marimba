import sys
from marimba import Marimba
import time

m = Marimba()
m.connect()

#volume = int(sys.argv[1])
box = int(sys.argv[1])
volume = int(sys.argv[3])
duration = float(sys.argv[4])
length = int(sys.argv[2])


print "playing box #", box
while True:
	sequence = [box for i in range(0, length)]
	print sequence
	m.playSequence(sequence, 0, duration)
	time.sleep(10)
#notes, delay, duration
