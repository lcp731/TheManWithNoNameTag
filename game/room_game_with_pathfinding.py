import stellar
import resources
import tools
import math
import itertools
import random

#Ramaraunt add constants
N_LEFT = 0
N_UP = 1
N_RIGHT = 2
N_DOWN = 3
D_LEFT_UP = 4
D_LEFT_DOWN =5
D_RIGHT_UP = 6
D_RIGHT_DOWN = 7

class GridTile(stellar.objects.Object):
	def __init__(self, x, y, tilesize=32):
		stellar.objects.Object.__init__(self)

		self.tilesize = tilesize
		self.grid_x = x
		self.grid_y = y

		if self.grid_y%5:
			sprite = random.choice(resources.ARRAY_TILE_FLOOR_64)
			self.blocked = True
		else:
			sprite = random.choice(resources.ARRAY_TILE_SHELVES_64)
			self.blocked = False

		self.add_sprite("default", sprite)
		self.set_sprite("default")

		#Ramaraunt PATHFINDING add
		self.neighbors = []

	def draw(self):
		self.get_current_sprite().draw(self.room, self.get_position(), self.scale)

	def _draw(self):
		pass

class Player(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)
		animated = stellar.sprites.Animation(*resources.IMGS)
		animated.xoffset = -32
		animated.yoffset = -32
		animated.set_rate(20)
		self.add_sprite("default", animated)
		self.set_sprite("default")

class Pather(stellar.objects.Object):
	def __init__(self, xcord, ycord):
		stellar.objects.Object.__init__(self)
		box = stellar.sprites.Box((100,0,0),32,32,-32,-32)
		self.add_sprite("default", box)
		self.set_sprite("default")
		self.roomx = xcord
		self.roomy = ycord

	def logic(self):
		pass

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.grid_dims = (100, 100)

		self.tilesize = 64

		self.cam_x = 0
		self.cam_y = 0
		self.move_speed = 10

		self.grid = stellar.pathfinding.Grid()

		for x, y in tools.itergrid(*self.grid_dims):
			nt = GridTile(x, y, tilesize=self.tilesize)
			nt.disable()
			self.add_object(nt)
			self.grid.tiles.append(nt)

		self.cambox_border = 192

		self.player = Player()
		self.add_object(self.player)

		self.pather = Pather()
		self.add_object(self.pather)


		#pathfinding stuff begin RAMARAUNT
		for x, y in tools.itergrid(*self.grid_dims):
			if x < self.grid_dims[0]:
				self.grid[x,y].neighbors.append((N_RIGHT,1.0))
			if x < self.grid_dims[1]:
				self.grid[x,y].neighbors.append((N_DOWN,1.0))
			if x > 0:
				self.grid[x,y].neighbors.append((N_LEFT,1.0))
			if y > 0:
				self.grid[x,y].neighbors.append((N_UP,1.0))
			if y > 0 and x > 0:
				self.grid[x,y].neighbors.append((D_LEFT_UP,1.2))
			if y > 0 and x < self.grid_dims[0]:
				self.grid[x,y].neighbors.append((D_RIGHT_UP,1.2))
			if y < self.grid_dims[1] and x > 0:
				self.grid[x,y].neighbors.append((D_LEFT_DOWN,1.2))
			if y < self.grid_dims[1] and x < self.grid_dims[1]:
				self.grid[x,y].neighbors.append((D_RIGHT_DOWN,1.2))

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

def gridPathfind(grid, startNode, endNode, nodeSize, patherSize):
	openList = []
	openListPriorities = []
	closedList = []
	curNode = startNode
	closedList.append(curNode)
	while curNode != endNode:
		for neighbor in curNode.neighbors:
			if not neighbor.blocked:
				if not neighbor in openList:
					neighbor.hScore= curNode.hScore + curNode.moveCosts[curNode.neighbors.index(neighbor)]
					neighbor.gscore = returnDistanceBetweenPoints(neighbor.x,endNode.x,neighbor.y,endNode.y)/nodeSize
					neighbor.mscore = neighbor.hscore + neighbor.gscore
					openList.append(neighbor)
					openListPriorities.append(neighbor.mscore)
				elif curNode.hScore + curNode.moveCosts[curNode.neighbors.index(neighbor)] < neighbor.hscore:
					del openListPriorities[openList.index(neighbor)]
					openList.remove(neighbor)
					neighbor.hscore = curNode.hScore + curNode.moveCosts[curNode.neighbors.index(neighbor)]
					neighbor.mscore = neighbor.hscore + neighbor.gscore
		if len(openList)==0:
			del openList
			del closedList
			return None
		else:
			minVal = 9999999999999
			minIndex = -1
			for index in range(0,len(openListPriorities)-1):
				if openListPriorities[index] < minVal:
					minIndex = Index
					minVal = openListPriorities[index]
			del openListPriorities[minIndex]
			newNode = openList[minIndex]
			openList.remove(newNode)
			newNode.parent = curNode
			curNode = newNode
			closedList.append(curNode)
	path = []
	while curNode != startNode:
		path.append([curNode.grid_x,curNode.grid_y])
		curNode.parent.child=cur_node
		curNode=curNode.parent
	del openList
	del closedList
	wipeNodes(grid)
	pathSmooth(grid, cords, nodeSize, patherSize),
	return cords

def pathSmooth(grid, path, nodeSize, patherSize):
	for point in reversed(path):
		for target in reversed(path):
			if path.index(point) < path.index(target):
				if checkIfCollide(grid, point, target, nodeSize, patherSize):
					for removable in range(path.index(target) - 1, path.index(point)):
						path.remove(path[removeable])
				

def checkIfCollide(grid, pointa, pointb, nodeSize, patherSize):
	returnvalue = False
	slope = pygame.tools.returnSlopeOfLineBetween(pointa, pointb)
	yIntercept = pygame.toosl.returnYIntercept(pointa, slope)

	points = []

	#get x'es
	for xcord in range(pointa[0],pointb[0]):
		points.append([xcord, pygame.tools.getYCordWithData(xcord,slope,yIntercept)])
	
	#get y's
	for ycord in range(pointa[1],pointb[1]):
		points.append([pygame.tools.getXCordWithData(ycord,slope,yIntercept), ycord])

	distance = patherSize/2
	for point in points:
		if 

def returnClosestTile(grid, halfNodeSize, point):
	for tiles in grid.tiles:
		if returnDistanceBetweenPoints(point[0],tile.x,point[1],tile.y)<halfNodeSize:
			return tile
	return False


