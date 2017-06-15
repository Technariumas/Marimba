#!/bin/bash
ttymidi -b 115200 -s /dev/serial0 &
sleep 1
cd /home/pi/Marimba
git pull
aplaymidi -p 128:1 /home/pi/Marimba/data_analysis/midi_output/play.mid &

/home/pi/Marimba/firmware/util/setupLights.py
/home/pi/Marimba/firmware/util/loadHighStrokes.py
/home/pi/Marimba/firmware/util/loadMidStrokes.py
/home/pi/Marimba/firmware/util/lights_control.py 
while :; do sleep 1; done
