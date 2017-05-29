#!/bin/bash
ttymidi -b 115200 -s /dev/serial0 &
cd /home/pi/Marimba/firmware/util
./highStrokeCalibrator.py all
killall ttymidi
