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
#notes, delay, duration, velocity
m.playSequence(sequence, 1.5, duration, volume)
time.sleep(10)
#notes, delay, duration
