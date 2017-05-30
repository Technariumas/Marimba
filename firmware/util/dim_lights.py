#!/usr/bin/python
from marimba import Marimba
from time import sleep

m = Marimba()
m.connect()

print("Dimming all lights...")

m.setLightMaximum(14, 60)# for n in range(80)]
sleep(1)
m.setLightMinimum(14, 59)# for n in range(80)]
sleep(1)

m.setLightCount(14, 8)# for n in range(80)]
sleep(1)
m.setLightStep(14, 1) #for n in range(80)]
'''
[m.setLightMaximum(n, 60) for n in range(80)]
sleep(1)
[m.setLightMinimum(n, 15) for n in range(80)]
sleep(1)
m.setLightStep(n, 7) for n in range(80)]
'''
