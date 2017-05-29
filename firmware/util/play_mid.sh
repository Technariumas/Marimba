ttymidi -b 115200 -s /dev/serial0 &
./play_boxes.py 60
killall ttymidi
