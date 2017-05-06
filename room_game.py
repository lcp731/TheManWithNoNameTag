import stellar
import resources
import tools

class GridTile(stellar.objects.Object):
	def __init__(self, x, y, tilesize=32):
		stellar.objects.Object.__init__(self)

		self.tilesize = tilesize

		self.add_sprite("default",
			stellar.sprites.Box(stellar.tools.random_rgb(), self.tilesize, self.tilesize)
		)
		self.set_sprite("default")

		self.grid_x = self.tilesize * x
		self.grid_y = self.tilesize * y

	def logic(self):
		self.x = self.grid_x + self.room.cam_x
		self.y = self.grid_y + self.room.cam_y

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.grid_dims = (32, 32)
		self.grid = {}

		self.cam_x = 0
		self.cam_y = 0
		self.cam_speed = 2

		for x, y in tools.itergrid(*self.grid_dims):
			nt = GridTile(x, y)
			self.add_object(nt)
			self.grid[x, y] = nt

	def control(self, buttons, mousepos):
		if buttons[stellar.keys.S_HELD][stellar.keys.K_w]:
			self.cam_y += self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_s]:
			self.cam_y -= self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_a]:
			self.cam_x += self.cam_speed
		if buttons[stellar.keys.S_HELD][stellar.keys.K_d]:
			self.cam_x -= self.cam_speed