import pygame
import math
import random
import inspect
import copy

pygame.init()

def rot_center(image, angle):
	"""rotate an image while keeping its center and size"""
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image

def clone(obj):
	return copy.copy(obj)

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
		game.draw_blit(text, posn)

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
	
def returnSlopeOfLineBetween(pointA, pointB):
	return float(pointB[1]-pointA[1])/(pointB[0]-pointA[0])

def returnYIntercept(point, slope):
	return (point[1] - (slope*point[0]))

def getYCordWithData(xcord, slope, yIntercept):
	return (xcord * slope) + yIntercept

def getXCordWithData(ycord, slope, yIntercept):
	return (ycord - yIntercept)/slope

def parse_level(path):
	level = {}
	with open(path, "rb") as file:
		reader = csv.reader(file)

		for y, row in enumerate(reader):
			for x, val in enumerate(row):
				val = val.split()
				level[x, y] = (int(val[0]), int(val[1]))

	return level

def load_sheet(image, *sections):
	sprites = []
	for section in sections:
		new = image.get_section(section)
		new.inherit(image)
		sprites.append(new)
	return sprites

def transform_sprites(array, scale):
	for spr in array:
		spr.perma_scale(scale)

def log(*msgs):
	msgs = map(str, msgs)
	frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[1]
	string = "[STELLAR] %s, %s - %s" % (function_name, filename, ", ".join(msgs))
	print string