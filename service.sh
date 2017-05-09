#!/bin/bash
ttymidi -b 115200 -s /dev/serial0 &
sleep 1
/home/pi/Marimba/firmware/util/blastem.py
