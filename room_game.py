import stellar
import resources
import tools

class GridTile(stellar.objects.Object):
	def __init__(self, x, y):
		stellar.objects.Object.__init__(self)

		self.add_sprite()

		self.grid_x = x
		self.grid_y = y

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.grid_dims = (32, 32)
		self.grid = {}

		for x, y in tools.itergrid(*self.grid_dims):
			nt = GridTile(x, y)
			self.grid[x, y] = nt

		print self.grid