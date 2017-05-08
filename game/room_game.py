import stellar
import resources
import tools
import math
import itertools
import random

class GridTile(stellar.objects.Object):
	def __init__(self, x, y, typ=0, tilesize=32):
		stellar.objects.Object.__init__(self)

		self.disable()

		self.tilesize = tilesize
		self.type = typ
		self.grid_x = x
		self.grid_y = y

		sprite = resources.TILE_REFERENCE[self.type]

		self.add_sprite("default", sprite)
		self.set_sprite("default")

	def draw(self):
		self.get_current_sprite().draw(self.room, self.get_position(), self.scale)

	def _draw(self):
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

class Enemy(GameObject):
	def __init__(self):
		GameObject.__init__(self)

class Player(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)
		animated = stellar.sprites.Animation(*resources._LEFTY)
		animated.xoffset = -32
		animated.yoffset = -32
		animated.set_rate(20)
		self.add_sprite("default", animated)
		self.set_sprite("default")

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)
		self.game_objects = []

		self.grid_dims = (100, 100)
		self.grid = {}

		self.tilesize = resources.TILESIZE

		self.cam_x = 0
		self.cam_y = 0
		self.move_speed = 10

		for x, y in resources.LEVEL_TEST:
			nt = GridTile(x, y, typ=resources.LEVEL_TEST[x, y], tilesize=self.tilesize)
			self.add_object(nt)
			self.grid[x, y] = nt

		self.gameobj = Enemy()
		self.gameobj.move_to(500, 500)
		self.gameobj.add_sprite("default", stellar.sprites.Box((255, 0, 0), 25, 25))
		self.gameobj.set_sprite("default")
		self.add_gameobject(self.gameobj)

		self.player = Player()
		self.add_object(self.player)

	def add_gameobject(self, obj):
		self.add_object(obj)
		self.game_objects.append(obj)

	def on_load(self):
		self.player.move_to(*self.center())

	# Manual draw function
	def _draw(self):
		self.game.screen.fill(self.background)

		drawbuffer = 1
		x_wid = int(math.ceil(self.size[0] / float(self.tilesize)))
		y_wid = int(math.ceil(self.size[1] / float(self.tilesize)))
		cam_gx = int(math.floor(self.cam_x / float(self.tilesize)))
		cam_gy = int(math.floor(self.cam_y / float(self.tilesize)))
		x_range = xrange(cam_gx-drawbuffer, cam_gx+x_wid+drawbuffer)
		y_range = xrange(cam_gy-drawbuffer, cam_gy+y_wid+drawbuffer)

		for x, y in itertools.product(x_range, y_range):
			try:
				obj = self.grid[x, y]
				obj.x = (x * self.tilesize) - self.cam_x
				obj.y = (y * self.tilesize) - self.cam_y
				obj.draw()
			except KeyError:
				pass

		for obj in self.game_objects:
			obj.x = obj.game_x - self.cam_x
			obj.y = obj.game_y - self.cam_y
			obj.draw()

		for fixture, posn in self.fixtures:
			fixture.draw(self, posn)

		for obj in self.objects:
			obj._draw()

		self.draw()

	def control(self, buttons, mousepos):
		deltaX = 0
		deltaY = 0

		if buttons[stellar.keys.S_HELD][stellar.keys.K_UP]:
			deltaY -= self.move_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_DOWN]:
			deltaY += self.move_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_LEFT]:
			deltaX -= self.move_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_RIGHT]:
			deltaX += self.move_speed

		if buttons[stellar.keys.S_PUSHED][stellar.keys.K_SPACE]:
			resources.AUDIO_GUNSHOT.play()

		self.cam_x += deltaX
		self.cam_y += deltaY