# Python MIDI over serial port

* ttymidi - compile from source
  * install bazaar - sudo apt install bzr
  * checkout from Launchpad repo - bzr branch lp:ttymidi
  * requires pthread - sudo apt install libpthread-stubs0-dev
  * requires libasound - sudo apt install libasound2-dev
  * needs a fix in Makefile - gcc src/ttymidi.c -o ttymidi -lasound -lpthread
* sudo apt install libportmidi0 sudo apt install libportmidi-dev
* pip install pygame 
* *OR* if 
* pygame - compile from source 
  * sdl is required - sudo apt install libsdl1.2-dev

## Example programs
Start ttymidi (read ttymidi README file of type ttymidi --help)

```
ttymidi -s /dev/ttyS0 -b 2400
```

This will print list of midi devices, note the number of ttymidi device
```
import pygame.midi
pygame.midi.init()
print([(n, pygame.midi.get_device_info(n)) for n in range(pygame.midi.get_count())])
```

Open port and stream into it:
```
import pygame.midi
pygame.midi.init()
out = pygame.midi.Output(3)
out.note_on(1)
out.note_off(1)
```
