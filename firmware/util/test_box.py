import sys
from marimba import Marimba
import time

m = Marimba()
m.connect()

box = int(sys.argv[1])
volume = int(sys.argv[2])
print "playing box #", box
m.test(box, volume, 0.0)


