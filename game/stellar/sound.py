import pyaudio
import wave
import pygame
import threading
import time

# Base 'Sound' class that all inherit from
class Sound:
	def __init__(self):
		self.path = None
		self.volume = 1

	def set_volume(self, val):
		self.volume = val

	def play(self):
		pass

# For sound effects, only supports WAV. Use this when you don't want any delay when playing the sound
class Effect(Sound):
	def __init__(self, path, chunk=1024):
		Sound.__init__(self)
		self.path = path
		self.chunk = chunk
		self.volume = 0

	def set_volume(self, val):
		self.volume = val

	def rms(self, data):
		count = len(data)/2
		format = "%dh"%(count)
		shorts = struct.unpack( format, data )
		sum_squares = 0.0
		for sample in shorts:
			n = sample * (1.0/32768)
			sum_squares += n*n
		return math.sqrt( sum_squares / count )

	def _play(self):
		wav = wave.open(self.path, "rb")
		audio = pyaudio.PyAudio()
		stream = audio.open(
			format=audio.get_format_from_width(wav.getsampwidth()),
			channels=wav.getnchannels(),
			rate=wav.getframerate(),
			output=True
		)

		data = wav.readframes(self.chunk)

		while data:
			stream.write(data)
			data = wav.readframes(self.chunk)

		stream.stop_stream()
		stream.close()

	def play(self):
		thread = threading.Thread(target=self._play)
		thread.start()

# For music, can only play one at a time, MP3 supported. Will have some slight lag starting up, so not for sound effects
class Music(Sound):
	def __init__(self, path):
		Sound.__init__(self)
		self.path = path
		self.looping = False

	def set_volume(self, val):
		self.volume = val
		pygame.mixer.music.set_volume(self.volume)

	def _play(self):
		pygame.mixer.init()
		pygame.mixer.music.load(self.path)
		if self.looping:
			pygame.mixer.music.play(-1)
		else:
			pygame.mixer.music.play()

	def play(self):
		thread = threading.Thread(target=self._play)
		thread.start()