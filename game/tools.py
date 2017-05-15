import itertools
import csv
import copy
import stellar

def itergrid(x, y):
	return itertools.product(xrange(x), xrange(y))

def base_type(var):
	try: return int(var)
	except ValueError:
		try: return float(var)
		except ValueError:
			return str(var)

class LoadedTile:
	def __init__(self, x, y, **attrs):
		self.x = x
		self.y = y
		self.attrs = attrs

	def __repr__(self):
		return "LoadedTile(%s, %s, %s)" % (self.x, self.y, self.attrs)

	def __getitem__(self, key):
		return self.attrs[key]

	def __setitem__(self, key, value):
		raise Exception("Tile setting not allowed")

def legacy_parse_level(path):
	level = {}
	with open(path, "rb") as file:
		reader = csv.reader(file)

		for y, row in enumerate(reader):
			for x, val in enumerate(row):
				val = val.split()
				level[x, y] = (int(val[0]), int(val[1]))

	return level

def parse_level(path):
	level = {}
	with open(path, "rb") as file:
		raw_lines = file.read().split("?")
		raw_lines = filter(lambda x: bool(x), raw_lines)

	raw_header = raw_lines[0]
	header = {}
	sep = raw_header.split("&")
	for dp in sep:
		sep2 = dp.split("=")
		header[sep2[0]] = base_type(sep2[1])
	lines = raw_lines[1:]

	for line, point in zip(lines, itergrid(header["Width"], header["Height"])):
		raw_attrs = line.split("&")
		attrs = {}
		for attr in raw_attrs:
			spl = attr.split("=")
			attrs[spl[0]] = base_type(spl[1])
		level[point] = LoadedTile(*point, **attrs)

	return level

def clone(obj):
	return copy.copy(obj)

def blank(*args, **kwargs):
	pass

class GameObject(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)

		self.game_x = 0
		self.game_y = 0

	def move_to(self, x, y):
		self.game_x = x
		self.game_y = y

	def move_by(self, dx, dy):
		self.game_x += dx
		self.game_y += dy

	def draw(self):
		self.get_current_sprite().draw(self.room, self.get_position(), self.scale)

	def _draw(self):
		pass