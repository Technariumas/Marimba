ttymidi -b 115200 -s /dev/serial0 &

python /home/pi/Marimba/firmware/util/dim_lights.py

killall ttymidi
