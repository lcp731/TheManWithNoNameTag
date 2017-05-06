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

	# def _draw(self):
	# 	self.get_current_sprite().draw(self.room, self.get_position(), self.scale)
	# 	self.draw()

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.grid_dims = (100, 100)
		self.grid = {}

		self.tilesize = 64

		self.cam_x = 0
		self.cam_y = 0
		self.cam_speed = 10

		for x, y in tools.itergrid(*self.grid_dims):
			nt = GridTile(x, y, tilesize=self.tilesize)
			nt.disable()
			self.add_object(nt)
			self.grid[x, y] = nt

	# Manual draw function
	def draw(self):
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
				obj._draw()
			except KeyError:
				pass

	def control(self, buttons, mousepos):
		if buttons[stellar.keys.S_HELD][stellar.keys.K_w]:
			self.cam_y -= self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_s]:
			self.cam_y += self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_a]:
			self.cam_x -= self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_d]:
			self.cam_x += self.cam_speed