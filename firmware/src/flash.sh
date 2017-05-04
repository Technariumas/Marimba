~/arduino-1.6.7/arduino --board arduino:avr:atmegang:cpu=atmega48 --pref build.path=./build --verify marimba/marimba.ino && avrdude -c usbasp -p atmega48 -U flash:w:build/marimba.ino.hex:i
