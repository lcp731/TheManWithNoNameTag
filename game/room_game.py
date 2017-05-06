import stellar
import resources
import tools
import math
import itertools
import random

class GridTile(stellar.objects.Object):
	def __init__(self, x, y, tilesize=32):
		stellar.objects.Object.__init__(self)

		self.tilesize = tilesize

		self.add_sprite("default",
			random.choice(resources.ARRAY_TILE_SHELVES_64)
		)
		self.set_sprite("default")

	def draw(self):
		self.get_current_sprite().draw(self.room, self.get_position(), self.scale)

	def _draw(self):
		pass

class Player(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)
		animated = stellar.sprites.Animation(*resources.IMGS)
		animated.set_rate(20)
		self.add_sprite("default", animated)
		self.set_sprite("default")

	def in_cambox(self):
		x_range = xrange(self.room.cambox_border, self.room.size[0]-self.room.cambox_border)
		y_range = xrange(self.room.cambox_border, self.room.size[1]-self.room.cambox_border)
		spr = self.get_current_sprite()
		return (self.x+(spr.size[0]/2) in x_range) and (self.y+(spr.size[0]/2) in y_range)

	def control(self, buttons, mousepos):
		if self.in_cambox():
			if buttons[stellar.keys.S_HELD][stellar.keys.K_UP]:
				self.y -= self.room.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_DOWN]:
				self.y += self.room.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_LEFT]:
				self.x -= self.room.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_RIGHT]:
				self.x += self.room.move_speed

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.grid_dims = (100, 100)
		self.grid = {}

		self.tilesize = 64

		self.cam_x = 0
		self.cam_y = 0
		self.move_speed = 10

		for x, y in tools.itergrid(*self.grid_dims):
			nt = GridTile(x, y, tilesize=self.tilesize)
			nt.disable()
			self.add_object(nt)
			self.grid[x, y] = nt

		self.cambox_border = 192

		self.player = Player()
		self.add_object(self.player)

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

		for fixture, posn in self.fixtures:
			fixture.draw(self, posn)

		for obj in self.objects:
			obj._draw()

		self.draw()

	def control(self, buttons, mousepos):
		stellar.log(self.player.in_cambox())
		if not self.player.in_cambox():
			if buttons[stellar.keys.S_HELD][stellar.keys.K_UP]:
				self.cam_y -= self.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_DOWN]:
				self.cam_y += self.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_LEFT]:
				self.cam_x -= self.move_speed
			if buttons[stellar.keys.S_HELD][stellar.keys.K_RIGHT]:
				self.cam_x += self.move_speed

		if buttons[stellar.keys.S_PUSHED][stellar.keys.K_SPACE]:
			resources.AUDIO_GUNSHOT.play()
