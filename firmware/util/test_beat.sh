ttymidi -b 115200 -s /dev/serial0 &
echo "box number, number of notes, volume, note duration" $1, $2, $3, $4
./test_beat.py $1 $2 $3 $4
killall ttymidi
