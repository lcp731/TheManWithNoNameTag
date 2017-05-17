import room_game
import tools

class Tile:
	def __init__(self, x, y, solid=False):
		self.x = x
		self.y = y
		self.solid = solid

grid = {}
for x, y in tools.itergrid(50, 50):
	grid[x, y] = Tile(x, y)

def get_next_step(grid, start, end):
	# do some magic
	return (0, 0)

print get_next_step(grid, (0, 0), (5, 5))