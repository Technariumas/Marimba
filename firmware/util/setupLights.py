#!/usr/bin/python

from marimba import Marimba
from random import randrange
from time import sleep

m = Marimba()
m.connect()

[m.setLightStep(n, 3) for n in range(80)]
sleep(1)
[m.setLightMaximum(n, 127) for n in range(80)]
sleep(1)
[m.setLightMaximum(n, 60) for n in [randrange(60, 80) for i in range(3)]]
sleep(1)
[m.setLightMaximum(n, 80) for n in [randrange(20, 60) for i in range(7)]]
sleep(1)
[m.setLightMaximum(n, 60) for n in [randrange(0, 20) for i in range(3)]]

