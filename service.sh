#!/bin/bash
ttymidi -b 115200 -s /dev/serial0 &
#sleep 1
#/home/pi/Marimba/firmware/util/blastem.py
cd /home/pi/Marimba
git pull
aplaymidi -p 128:1 /home/pi/Marimba/data_analysis/midi_output/play.mid &
cd /home/pi/Marimba/firmware/util
python lights_control.py 


