#!/bin/bash
ttymidi -b 57600 -s /dev/serial0 &
cd /home/pi/Marimba/firmware/util
./loadHighStrokes.py
killall ttymidi
