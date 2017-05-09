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

class Player(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)

		self.xoffset = -42
		self.yoffset = -56

		self.direction = 2
		self.face_direction = 2
		self.m_direction = 1
		self.backwards = False
		self.moving = False

		spr_standing_forward_l = stellar.sprites.Animation(*resources.LEFTY_STAND_FORWARD_L)
		spr_standing_backward_l = stellar.sprites.Animation(*resources.LEFTY_STAND_BACKWARD_L)
		spr_standing_forward_r = stellar.sprites.Animation(*resources.LEFTY_STAND_FORWARD_R)
		spr_standing_backward_r = stellar.sprites.Animation(*resources.LEFTY_STAND_BACKWARD_R)

		spr_running_fl = stellar.sprites.Animation(*resources.LEFTY_RUN_FL)
		spr_running_fr = stellar.sprites.Animation(*resources.LEFTY_RUN_FR)
		spr_running_bl = stellar.sprites.Animation(*resources.LEFTY_RUN_BL)
		spr_running_br = stellar.sprites.Animation(*resources.LEFTY_RUN_BR)

		spr_backward_fl = stellar.sprites.Animation(*resources.LEFTY_BACK_FL)
		spr_backward_fr = stellar.sprites.Animation(*resources.LEFTY_BACK_FR)
		spr_backward_bl = stellar.sprites.Animation(*resources.LEFTY_BACK_BL)
		spr_backward_br = stellar.sprites.Animation(*resources.LEFTY_BACK_BR)

		spr_standing_forward_l.set_rate(30)
		spr_standing_backward_l.set_rate(30)
		spr_standing_forward_r.set_rate(30)
		spr_standing_backward_r.set_rate(30)
		spr_running_bl.set_rate(5)
		spr_running_br.set_rate(5)
		spr_running_fl.set_rate(5)
		spr_running_fr.set_rate(5)
		spr_backward_fl.set_rate(5)
		spr_backward_fr.set_rate(5)
		spr_backward_bl.set_rate(5)
		spr_backward_br.set_rate(5)

		self.add_sprite("standing_forward_l", spr_standing_forward_l)
		self.add_sprite("standing_backward_l", spr_standing_backward_l)
		self.add_sprite("standing_forward_r", spr_standing_forward_r)
		self.add_sprite("standing_backward_r", spr_standing_backward_r)
		self.add_sprite("running_fl", spr_running_fl)
		self.add_sprite("running_fr", spr_running_fr)
		self.add_sprite("running_bl", spr_running_bl)
		self.add_sprite("running_br", spr_running_br)
		self.add_sprite("backward_fl", spr_backward_fl)
		self.add_sprite("backward_fr", spr_backward_fr)
		self.add_sprite("backward_bl", spr_backward_bl)
		self.add_sprite("backward_br", spr_backward_br)
		self.set_sprite("running_fl")

	def logic(self):
		# One hell of an if statement
		# PS: it's for sprite selection just ignore it
		if self.moving:
			if self.m_direction == 0:
				if self.face_direction == 0:
					if self.direction in [8, 1, 2]:
						self.set_sprite("running_bl")
					else:
						self.set_sprite("backward_bl")
				if self.face_direction == 3:
					if self.direction in [6, 7, 8]:
						self.set_sprite("running_fl")
					else:
						self.set_sprite("backward_fl")
			if self.m_direction == 1:
				if self.face_direction == 0:
					if self.direction in [8, 1, 2]:
						self.set_sprite("running_bl")
					else:
						self.set_sprite("backward_bl")
				if self.face_direction == 1:
					if self.direction in [2, 3, 4]:
						self.set_sprite("running_br")
					else:
						self.set_sprite("backward_br")
			if self.m_direction == 2:
				if self.face_direction == 1:
					if self.direction in [2, 3, 4]:
						self.set_sprite("running_br")
					else:
						self.set_sprite("backward_br")
				if self.face_direction == 2:
					if self.direction in [4, 5, 6]:
						self.set_sprite("running_fr")
					else:
						self.set_sprite("backward_fr")
			if self.m_direction == 3:
				if self.face_direction == 2:
					if self.direction in [4, 5, 6]:
						self.set_sprite("running_fr")
					else:
						self.set_sprite("backward_fr")
				if self.face_direction == 3:
					if self.direction in [6, 7, 8]:
						self.set_sprite("running_fl")
					else:
						self.set_sprite("backward_fl")

		else:
			if self.face_direction == 0:
				self.set_sprite("standing_backward_l")
			if self.face_direction == 1:
				self.set_sprite("standing_backward_r")
			if self.face_direction == 2:
				self.set_sprite("standing_forward_r")
			if self.face_direction == 3:
				self.set_sprite("standing_forward_l")

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)
		self.game_objects = []

		self.grid = {}

		self.tilesize = resources.TILESIZE


		self.cam_x = 0
		self.cam_y = 0
		self.move_speed = 8

		for x, y in resources.LEVEL_TEST:
			nt = GridTile(x, y, typ=resources.LEVEL_TEST[x, y], tilesize=self.tilesize)
			self.add_object(nt)
			self.grid[x, y] = nt


		self.player = Player()
		self.add_object(self.player)

	def line_pos(self, x):
		b = self.size[1]
		return (-self.slope * x) + b

	def line_neg(self, x):
		return self.slope * x

	def add_gameobject(self, obj):
		self.add_object(obj)
		self.game_objects.append(obj)

	def on_load(self):
		self.player.move_to(*self.center())
		self.slope = self.size[1]/float(self.size[0])

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
		mouseX, mouseY = mousepos
		deltaX = 0
		deltaY = 0

		if buttons[stellar.keys.S_HELD][resources.CONTROL_UP]:
			deltaY -= self.move_speed
		if buttons[stellar.keys.S_HELD][resources.CONTROL_DOWN]:
			deltaY += self.move_speed
		if buttons[stellar.keys.S_HELD][resources.CONTROL_LEFT]:
			deltaX -= self.move_speed
		if buttons[stellar.keys.S_HELD][resources.CONTROL_RIGHT]:
			deltaX += self.move_speed

		if deltaY < 0:
			if deltaX < 0:
				self.player.direction = 1
			elif deltaX > 0:
				self.player.direction = 3
			else:
				self.player.direction = 2
		elif deltaY > 0:
			if deltaX < 0:
				self.player.direction = 7
			elif deltaX > 0:
				self.player.direction = 5
			else:
				self.player.direction = 6
		else:
			if deltaX < 0:
				self.player.direction = 8
			elif deltaX > 0:
				self.player.direction = 4
			else:
				self.player.direction = 0

		midX, midY = self.center()
		if mouseY < midY:
			if mouseX < midX:
				self.player.face_direction = 0
			else:
				self.player.face_direction = 1
		else:
			if mouseX < midX:
				self.player.face_direction = 3
			else:
				self.player.face_direction = 2

		self.player.moving = bool(self.player.direction)

		pos = self.line_pos(mouseX) > mouseY
		neg = self.line_neg(mouseX) > mouseY

		if (pos) and (not neg):
			self.player.m_direction = 0
		if (pos) and (neg):
			self.player.m_direction = 1
		if (not pos) and (neg):
			self.player.m_direction = 2
		if (not pos) and (not neg):
			self.player.m_direction = 3

		self.cam_x += deltaX
		self.cam_y += deltaY

	def draw(self):
		self.draw_rect((255, 255, 255), list(self.center()) + [3, 3])
