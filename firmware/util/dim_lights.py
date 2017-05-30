#!/usr/bin/python
from marimba import Marimba

m = Marimba()
m.connect()

print("Dimming all lights...")

m.setLightMaximum(4, 40)# for n in range(80)]
sleep(1)
m.setLightMinimum(4, 40)# for n in range(80)]
sleep(1)
m.setLightStep(4, 7)# for n in range(80)]


'''
[m.setLightMaximum(n, 60) for n in range(80)]
sleep(1)
[m.setLightMinimum(n, 15) for n in range(80)]
sleep(1)
m.setLightStep(n, 7) for n in range(80)]
'''
