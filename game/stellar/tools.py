import pygame
import math
import random
import inspect

pygame.init()

class Font(pygame.font.Font):
	def __init__(self, path, size, color, background=None, antialias=True, underline=False, bold=False, italic=False):
		pygame.font.Font.__init__(self, path, size)

		self.set_underline(underline)
		self.set_bold(bold)
		self.set_italic(italic)
		self.color = color
		self.background = background
		self.antialias = antialias

	def get_surf(self, text):
		return self.render(text, self.antialias, self.color)

	def draw(self, game, text, posn):
		# background=self.background
		text = self.get_surf(text)
		game.screen.blit(text, posn)

class Cooldown:
	def __init__(self, duration):
		self.duration = duration
		self.clock = duration

	def frame(self):
		self.clock -= 1

	def reset(self):
		self.clock = self.duration

	def is_done(self):
		return self.clock <= 0

def returnDistanceBetweenPoints(x1, x2, y1, y2):
    return math.sqrt((x1-x2)^2 + (y1-y2)^2)

def random_rgb():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return r, g, b

def scale_image(image, **kwargs):
	image.perma_scale(**kwargs)
	return image

def log(*msgs):
	msgs = map(str, msgs)
	frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[1]
	string = "[STELLAR] %s, %s - %s" % (function_name, filename, ", ".join(msgs))
	print string

def load_sheet(image, *sections):
	sprites = []
	for section in sections:
		new = image.get_section(section)
		sprites.append(new)
	return sprites

def transform_sprites(array, scale):
	for spr in array:
		spr.perma_scale(scale)