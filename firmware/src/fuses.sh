
#!/bin/bash
avrdude -c usbasp -p atmega48 -U hfuse:w:0xDF:m -U lfuse:w:0xC7:m -U efuse:w:0xFF:m
