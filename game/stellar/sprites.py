import pygame
import hitboxes

class Sprite:
	def __init__(self, xoffset=0, yoffset=0):
		self.xoffset = xoffset
		self.yoffset = yoffset
		self.size = (0, 0)

		self.hitbox = hitboxes.Hitbox()

	def draw(self, room, posn, scale=1):
		pass

class Box(Sprite):
	def __init__(self, color, width, height, xoffset=0, yoffset=0):
		Sprite.__init__(self, xoffset=xoffset, yoffset=yoffset)
		self.width = width
		self.height = height
		self.size = (self.width, self.height)
		self.color = color

				
		self.hitbox = hitboxes.Box(self.width, self.height)

	def draw(self, room, posn, scale=1):
		posn = (posn[0]+self.xoffset, posn[1]+self.yoffset)
		room.draw_rect(self.color, list(posn) + [self.width*scale, self.height*scale])

class BoxOutline(Sprite):
	def __init__(self, color, width, height, xoffset=0, yoffset=0, linewidth=1):
		Sprite.__init__(self, xoffset=xoffset, yoffset=yoffset)
		self.width = width
		self.height = height
		self.size = (self.width, self.height)
		self.color = color
		self.lines = [(0,0),(width,0),(width,height),(0,height)]
		self.linewidth = linewidth
		self.hitbox = hitboxes.Box(self.width, self.height)

	def draw(self, room, posn, scale=1):
		posn = (posn[0]+self.xoffset, posn[1]+self.yoffset)
		finallines = []
		for point in range(4):
			curpoint = (self.lines[point][0] + posn[0],self.lines[point][1]+posn[1])
			finallines.append(curpoint)
		room.draw_lines(self.color, finallines, self.linewidth)

class Ellipse(Sprite):
	def __init__(self, color, width, height, xoffset=0, yoffset=0):
		Sprite.__init__(self, xoffset=xoffset, yoffset=yoffset)
		self.width = width
		self.height = height
		self.size = (self.width, self.height)
		self.color = color

		self.hitbox = hitboxes.Ellipse(self.width, self.height)

	def draw(self, room, posn, scale=1):
		posn = (posn[0]+self.xoffset, posn[1]+self.yoffset)
		room.draw_ellipse(self.color, list(posn) + [self.width*scale, self.height*scale])

class Image(Sprite):
	def __init__(self, path, dimensions=None, xoffset=0, yoffset=0):
		Sprite.__init__(self, xoffset=xoffset, yoffset=yoffset)

		if isinstance(path, pygame.Surface):
			self.path = None
			self.surf = path
		else:
			self.path = path
			self.surf = pygame.image.load(self.path)

		if dimensions:
			self.surf = pygame.transform.scale(self.surf, dimensions)

		self.size = self.surf.get_rect().size

		self.hitbox = hitboxes.Box(*self.size)

	def get_section(self, section):
		cropped = pygame.Surface(section[-2:])
		cropped.blit(self.surf, (0, 0), section)
		new = Image(cropped)
		return new

	# When it's permenant and you don't want performance to take a hit
	def perma_scale(self, scale=None, width=None, height=None):
		if scale:
			size = map(lambda x: int(x*scale), self.size)
		else:
			size = (width, height)
		self.surf = pygame.transform.scale(self.surf, size)
		return self

	def replace_color(self, find_color, replace_color):
		for x in xrange(self.size[0]):
			for y in xrange(self.size[1]):
				if self.surf.get_at([x, y]) == find_color:
					self.surf.set_at([x, y], replace_color)

	def draw(self, room, posn, scale=1):
		posn = (posn[0]+self.xoffset, posn[1]+self.yoffset)
		if scale != 1:
			size = map(lambda x: int(x*scale), self.size)
			img = pygame.transform.scale(self.surf, size)
		room.draw_blit(self.surf, posn)

class Text(Sprite):
	def __init__(self, text, font, xoffset=0, yoffset=0):
		Sprite.__init__(self, xoffset=xoffset, yoffset=yoffset)
		self.text = text
		self.font = font
		self.surf = self.font.get_surf(self.text)
		self.size = self.font.size(self.text)

		self.hitbox = hitboxes.Box(*self.size)

	def draw(self, room, posn, scale=1):
		posn = (posn[0]+self.xoffset, posn[1]+self.yoffset)
		size = map(lambda x: int(x*scale), self.size)
		txt = pygame.transform.scale(self.surf, size)
		room.draw_blit(txt, posn)

class Compound(Sprite):
	def __init__(self, *sprites):
		Sprite.__init__(self)
		self.sprites = sprites

		allboxes = []
		for sprite in self.sprites:
			allboxes.append(sprite.hitbox)
		self.hitbox = hitboxes.Compound(*allboxes)

	def draw(self, room, posn, scale=1):
		for sprite in self.sprites:
			sprite.draw(room, posn)

def LoadSheet(image, *sections):
	pygame.init()
	sprites = []
	for section in sections:
		new = image.get_section(section)
		sprites.append(new)
	return sprites

class Animation(Sprite):
	def __init__(self, *sprites):
		Sprite.__init__(self)
		self.sprites = sprites
		self.frames = len(self.sprites)
		self.rate = 60
		self.counter = 0
		self.frame = 0
		self.amimated = True

	def pause(self):
		self.amimated = False

	def resume(self):
		self.amimated = True

	def set_rate(self, rate):
		self.rate = rate

	def draw(self, room, posn, scale=1):
		self.frame = (self.counter / self.rate) % self.frames
		self.sprites[self.frame].xoffset = self.xoffset
		self.sprites[self.frame].yoffset = self.yoffset
		self.sprites[self.frame].draw(room, posn, scale=scale)
		self.size = self.sprites[self.frame].size
		self.counter += 1