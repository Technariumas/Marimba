import pygame.midi
import time

class Marimba:
	CHANNEL_SOLENOIDS = 0
	CHANNEL_PARAM_LED_STEP = 1
	CHANNEL_PARAM_LED_MINIMUM = 2
	CHANNEL_PARAM_LED_MAXIMUM = 3
	CHANNEL_PARAM_LED_COUNT = 4
	CHANNEL_PARAM_STROKE_HIGH_LENGTH = 5
	CHANNEL_PARAM_STROKE_MID_LENGTH = 6
	CHANNEL_PARAM_DAMPER_ENGAGE_DELAY = 7
	CHANNEL_PARAM_DAMPER_PRESS_LENGTH = 8
	CHANNEL_PARAM_DAMPER_MAX_DRIVE = 9

	output = None
	def connect(self):
		pygame.midi.quit()
		pygame.midi.init()
		midiDevices = [(n, pygame.midi.get_device_info(n)) for n in range(pygame.midi.get_count())]
		for d in midiDevices:
			if d[1][1] == "ttyMIDI" and 1 == d[1][3]:
				id = d[0]
				self.output = pygame.midi.Output(id)
				return
		raise Exception("Can't find 'ttyMIDI' device. Is ttymidi utility runing?")

	def play(self, id, velocity = 127):
		self.output.note_on(note=id, velocity=velocity, channel=0)

	def stop(self, id):
		self.output.note_off(note=id, channel=1)

	def setHighStrokeLength(self, id, lengthMs = 17):
		self.output.note_on(channel=self.CHANNEL_PARAM_STROKE_HIGH_LENGTH, note=id, velocity=lengthMs)
		self.test(id=id, velocity=127)

	def setMidStrokeLength(self, id, lengthMs = 60):
		self.output.note_on(channel=self.CHANNEL_PARAM_STROKE_MID_LENGTH, note=id, velocity=lengthMs)
		self.test(id=id, velocity=1)

	def setDamperEngageDelay(self, id, lengthMs = 3):
		self.output.note_on(channel=self.CHANNEL_PARAM_DAMPER_ENGAGE_DELAY, note=id, velocity=lengthMs)
		self.test(id=id, velocity=127)

	def setDamperPressLength(self, id, lengthMs = 300):
		self.output.note_on(channel=self.CHANNEL_PARAM_DAMPER_PRESS_LENGTH, note=id, velocity=lengthMs)
		self.test(id=id, velocity=127)

	def setDamperMaxDrive(self, id, drive=128):
		self.output.note_on(channel=self.CHANNEL_PARAM_DAMPER_MAX_DRIVE, note=id, velocity=drive)
		self.test(id=id, velocity=127)

	def test(self, id, velocity=127, delay=1):
		self.play(id=id, velocity=127)
		time.sleep(delay)
		self.stop(id=id)

	def playSequence(self, notes, delay):
		for note in notes:
			self.play(id=note, velocity=127)
			time.sleep(delay)
		time.sleep(5)
		for note in notes:
			self.stop(id=note)
