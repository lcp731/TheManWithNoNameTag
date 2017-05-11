import stellar
import resources
import tools
import math

class Player(stellar.objects.Object):
	def __init__(self, arm):
		stellar.objects.Object.__init__(self)

		self.arm = arm

		self.xoffset = -42
		self.yoffset = -56

		self.direction = 2
		self.direction_persistant = 2
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

		self.count = 0

	def move_to(self, x, y):
		self.x = x
		self.y = y
		self.arm.move_to(x, y)

	def move_by(self, x, y):
		self.x += x
		self.y += y
		self.arm.move_by(x, y)

	def logic(self):
		if not self.moving:
			if self.m_direction == 0:
				self.arm.set_sprite("left")
				if self.face_direction == 1:
					pass
				else:
					x, y = self.get_position()
					self.arm.move_to(x-47, y-75)

		if self.m_direction == 1:
			pass
		if self.m_direction == 2:
			self.arm.set_sprite("right")
		if self.m_direction == 3:
			pass

		# One hell of an if statement
		# PS: it's for sprite selection just ignore it
		backwards = False
		if self.moving:
			if self.m_direction == 0:
				if self.face_direction == 0:
					if self.direction in [7, 8, 1, 2]:
						self.set_sprite("running_bl")
					else:
						self.set_sprite("backward_bl")
						backwards = True
				if self.face_direction == 3:
					if self.direction in [6, 7, 8, 1]:
						self.set_sprite("running_fl")
					else:
						self.set_sprite("backward_fl")
						backwards = True 
			if self.m_direction == 1:
				if self.face_direction == 0:
					if self.direction in [8, 1, 2]:
						self.set_sprite("running_bl")
					else:
						self.set_sprite("backward_bl")
						backwards = True
				if self.face_direction == 1:
					if self.direction in [2, 3, 4]:
						self.set_sprite("running_br")
					else:
						self.set_sprite("backward_br")
						backwards = True
			if self.m_direction == 2:
				if self.face_direction == 1:
					if self.direction in [2, 3, 4, 5]:
						self.set_sprite("running_br")
					else:
						self.set_sprite("backward_br")
						backwards = True
				if self.face_direction == 2:
					if self.direction in [3, 4, 5, 6]:
						self.set_sprite("running_fr")
					else:
						self.set_sprite("backward_fr")
						backwards = True
			if self.m_direction == 3:
				if self.face_direction == 2:
					self.set_sprite("downright")
					if self.direction in [4, 5, 6]:
						self.set_sprite("running_fr")
					else:
						self.set_sprite("backward_fr")
						backwards = True
				if self.face_direction == 3:
					self.set_sprite("downleft")
					if self.direction in [6, 7, 8]:
						self.set_sprite("running_fl")
					else:
						self.set_sprite("backward_fl")
						backwards = True
		else:
			if self.face_direction == 0:
				self.set_sprite("standing_backward_l")
			if self.face_direction == 1:
				self.set_sprite("standing_backward_r")
			if self.face_direction == 2:
				self.set_sprite("standing_forward_r")
			if self.face_direction == 3:
				self.set_sprite("standing_forward_l")

		if self.direction:
			self.direction_persistant = self.direction

		self.backwards = backwards

class PlayerArm(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)

		# self.add_sprite("down", resources.LEFTY_ARM_DOWN)
		# self.add_sprite("downleft", resources.LEFTY_ARM_DOWNLEFT)
		# self.add_sprite("downright", resources.LEFTY_ARM_DOWNRIGHT)
		self.add_sprite("left", resources.LEFTY_ARM_LEFT)
		self.add_sprite("right", resources.LEFTY_ARM_RIGHT)
		# self.add_sprite("up", resources.LEFTY_ARM_UP)
		# self.add_sprite("upleft", resources.LEFTY_ARM_UPLEFT)
		# self.add_sprite("upright", resources.LEFTY_ARM_UPRIGHT)

		self.set_sprite("left")

	# def _draw(self):
	# 	ogrect = self.get_current_sprite().orig_surf.get_rect()
	# 	rect = self.get_current_sprite().surf.get_rect()
	# 	x, y = self.get_position()
	# 	x -= rect.width
	# 	y -= rect.height

	# 	self.get_current_sprite().draw(self.room, (x, y), self.scale)

	def _draw(self):
		pass

	def control(self, buttons, pos):
		mouseX, mouseY = pos
		playerX, playerY = self.room.center()

		angle = math.atan2(playerX-mouseX, playerY-mouseY)
		angle = math.degrees(angle)

		if self.current_sprite == "left":
			angle = angle - 90
		else:
			angle = angle + 90
		self.get_current_sprite().tilt(angle)

class PlayerMovementHitbox(stellar.objects.Object):
	def __init__(self, player):
		stellar.objects.Object.__init__(self)
		self.player = player
		self.width, self.height = self.player.get_current_sprite().current().size
		self.width *= resources.LEFTY_SCALE
		self.width *= 0.85
		self.height *= resources.LEFTY_SCALE
		self.height /= 2.0
		self.add_sprite("default", stellar.sprites.Box((255, 0, 0), self.width, self.height))
		self.set_sprite("default")

		self.get_current_sprite().draw = tools.blank

	def check_valid(self, deltaX, deltaY):
		cam_x = self.room.cam_x
		cam_y = self.room.cam_y

		newdeltaX = deltaX
		newdeltaY = deltaY

		nxt_tile_x_left = int( ( (cam_x + deltaX + (self.width/2)) / self.room.tilesize ) + ( self.room.size[0] / self.room.tilesize / 2 ) )
		nxt_tile_x_right = int( ( (cam_x + deltaX - (self.width/2)) / self.room.tilesize ) + ( self.room.size[0] / self.room.tilesize / 2 ) )
		nxt_tile_y_up = int( ( (cam_y + deltaY) / self.room.tilesize ) + ( self.room.size[1] / self.room.tilesize / 2 ) )
		nxt_tile_y_down = int( ( (cam_y + deltaY + self.height) / self.room.tilesize ) + ( self.room.size[1] / self.room.tilesize / 2 ) )


		cur_tile_x = int( ( (cam_x) / self.room.tilesize ) + ( self.room.size[0] / self.room.tilesize / 2 ) )
		cur_tile_y = int( ( (cam_y) / self.room.tilesize ) + ( self.room.size[1] / self.room.tilesize / 2 ) )

		x_left = self.room.grid[nxt_tile_x_left, cur_tile_y]
		x_right = self.room.grid[nxt_tile_x_right, cur_tile_y]
		y_up = self.room.grid[cur_tile_x, nxt_tile_y_up]
		y_down = self.room.grid[cur_tile_x, nxt_tile_y_down]

		x_range = xrange(int(self.x), int(self.x+self.width))
		y_range = xrange(int(self.y), int(self.y+self.height))

		if deltaY < 0:	# up
			if y_up.solid:
				newdeltaY = 0
		if deltaY > 0:	# down
			if y_down.solid:
				newdeltaY = 0
		if deltaX < 0:	# left
			if x_right.solid:	# YEAH I screwed up the directions
				newdeltaX = 0		# honestly idk why but it works so dont touch it lmao
		if deltaX > 0:	# right
			if x_left.solid:
				newdeltaX = 0

		return newdeltaX, newdeltaY