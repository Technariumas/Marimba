import sys
from marimba import Marimba
import time

m = Marimba()
m.connect()

#volume = int(sys.argv[1])
box = int(sys.argv[1])
duration = int(sys.argv[3])

print "playing box #", box
while True:
	m.test(box, volume, 0.0)

