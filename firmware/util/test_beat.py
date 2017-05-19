import sys
from marimba import Marimba
import time

m = Marimba()
m.connect()

box = int(sys.argv[1])
length = int(sys.argv[2])
volume = int(sys.argv[3])
duration = float(sys.argv[4])

print "Usage: python test_beat.py [box number] [number of notes] [volume] [duration]"
print "playing box #", box
sequence = [box for i in range(0, length)]
print sequence
m.playSequence(sequence, 0, duration)
time.sleep(10)
#notes, delay, duration
