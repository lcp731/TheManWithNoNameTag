import stellar
import resources
import tools
import math
import itertools
import random
import numpy
import uiobjects
import player

class GridTile(stellar.objects.Object):
	def __init__(self, x, y, typ=0, tilesize=32):
		stellar.objects.Object.__init__(self)

		self.disable()

		self.tilesize = tilesize
		self.type = typ
		self.grid_x = x
		self.grid_y = y

		self.solid = self.type in resources.SOLID_SPRITES
		self.bullet_solid = self.solid

		sprite = resources.TILE_REFERENCE[self.type]

		self.add_sprite("default", sprite)
		# self.add_sprite("blank", resources.TILE_REFERENCE[0, 0])
		self.set_sprite("default")

	def draw(self):
		self.get_current_sprite().draw(self.room, self.get_position(), self.scale)

	def _draw(self):
		pass

class Bullet(tools.GameObject):
	def __init__(self, sx, sy, target):
		tools.GameObject.__init__(self)

		stellar.log("Bullet shot from (%s, %s)" % (sx, sy))

		self.start_x = sx
		self.start_y = sy
		self.target_x, self.target_y = target

		self.speed = 30
		self.lifespan = 1000
		self.age = 0

		self.move_to(self.start_x, self.start_y)

		self.add_sprite("default", resources.BULLET)
		self.set_sprite("default")

		steps_number = max( abs(self.target_x-self.start_x), abs(self.target_y-self.start_y) )

		self.ostepx = float(self.target_x-self.start_x)/steps_number
		self.ostepy = float(self.target_y-self.start_y)/steps_number

		self.step_x = self.ostepx * self.speed
		self.step_y = self.ostepy * self.speed

		# for i in range(steps_number+1):
		# 	self.steps.append((int(self.start_x + stepx*i), int(self.start_y + stepy*i)))

	def kill(self, reason="unspecified"):
		stellar.log("Bullet killed, reason: %s" % reason)
		self.disable()

	def check_life(self):
		if self.age > self.lifespan:
			self.kill(reason="old age")
			return

		curtilex = int(self.game_x / self.room.tilesize)
		curtiley = int(self.game_y / self.room.tilesize)

		try:
			if self.room.grid[curtilex, curtiley].bullet_solid:
				self.kill(reason="hit wall")
				return
		except KeyError:
			self.kill(reason="out of map")
			return

		for zomb in self.room.zombies:
			if zomb.point_inside(self.get_position()):
				zomb.shot()
				self.kill(reason="hit enemy")
				return

	def logic(self):
		if not self.room.paused:
			for _i in xrange(self.speed):
				self.move_by(self.ostepx, self.ostepy)
				self.age += 1
				self.check_life()
				if not self.enabled:
					break

class Zombie(tools.GameObject):
	def __init__(self):
		tools.GameObject.__init__(self)
		self.move_speed = 20

		self.health = random.randint(3, 5)

		walk_left = stellar.sprites.Animation(*resources.ZOMBIE_LEFT)
		walk_right = stellar.sprites.Animation(*resources.ZOMBIE_RIGHT)

		walk_left.set_rate(5)
		walk_right.set_rate(5)

		walk_left.add_event([3, 5, 7], self.step_left)
		walk_right.add_event([3, 5, 7], self.step_right)

		self.add_sprite("walk_left", walk_left)
		self.add_sprite("walk_right", walk_right)
		self.set_sprite("walk_right")

	def kill(self, reason="unspecified"):
		self.room.zombies.remove(self)
		self.room.game_objects.remove(self)
		stellar.log("Zombie died, reason: %s" % reason)
		self.disable()

	def shot(self):
		self.health -= 1
		if self.health:
			stellar.log("Zombie got shot, %s health remaining" % self.health)
		else:
			self.kill(reason="shot")

	def step_left(self):
		# self.move_by(-self.move_speed, 0)
		pass

	def step_right(self):
		# self.move_by(self.move_speed, 0)
		pass

	def logic(self):
		if not self.room.paused:
			self.move_by(1, 0)

class Kiddo(tools.GameObject):
	def __init__(self):
		tools.GameObject.__init__(self)

		run_left = stellar.sprites.Animation(*resources.KIDDO_RUN_LEFT)
		run_right = stellar.sprites.Animation(*resources.KIDDO_RUN_RIGHT)
		help_left = stellar.sprites.Animation(*resources.KIDDO_HELP_LEFT)
		help_right = stellar.sprites.Animation(*resources.KIDDO_HELP_LEFT)

		run_left.set_rate(5)
		run_right.set_rate(5)
		help_left.set_rate(20)
		help_right.set_rate(20)

		self.add_sprite("run_left", run_left)
		self.add_sprite("run_right", run_right)

		self.add_sprite("help_left", help_left)
		self.add_sprite("help_right", help_right)

		self.set_sprite("help_left")

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)
		self.game_objects = []
		self.zombies = []
		self.bullets = []

		self.paused = False

		self.grid = {}

		self.tilesize = float(resources.TILESIZE)

		self.shoot_cooldown = stellar.tools.Cooldown(20)

		self.cam_x = 0
		self.cam_y = 0

		self.max_speed = 9
		self.slowed_speed = 7

		self.move_speed = self.max_speed

		for tile_pos in resources.LEVEL:
			tile = resources.LEVEL[tile_pos]
			x, y = tile.x, tile.y
			typ = tile["tile"]
			nt = GridTile(x, y, typ=typ, tilesize=self.tilesize)
			nt.room = self
			self.grid[x, y] = nt

		for tile_pos in self.grid:
			tile = self.grid[tile_pos]
			try:
				lower_tile = self.grid[tile_pos[0], tile_pos[1]+1]
				if not lower_tile.solid:
					tile.bullet_solid = False
			except KeyError:
				pass


		self.playerarm = player.PlayerArm()
		self.player = player.Player(self.playerarm)
		self.playerhb = player.PlayerMovementHitbox(self.player)
		self.add_object(self.player)
		self.add_object(self.playerarm)
		self.add_object(self.playerhb)

		self.kiddo = Kiddo()
		self.add_gameobject(self.kiddo)

		self.add_zombie(300, 300)

		# self.add_object(uiobjects.Revolver())

		self.menu_init()

	def pause(self):
		self.paused = True
		self.menu_open()

	def unpause(self):
		self.paused = False
		self.menu_close()

	def menu_init(self):
		self.menu = {
			"grey": uiobjects.GreyOut()
		}
		for el in self.menu:
			self.menu[el].disable()
			self.add_object(self.menu[el])

	def menu_open(self):
		for el in self.menu:
			self.menu[el].enable()

	def menu_close(self):
		for el in self.menu:
			self.menu[el].disable()

	def menu_step(self, buttons, mousepos):
		for el in self.menu:
			obj = self.menu[el]
			obj._logic()
			obj._control(buttons, mousepos)
			obj._draw()

	def add_zombie(self, *posn):
		nz = Zombie()
		nz.move_to(*posn)
		self.zombies.append(nz)
		self.add_gameobject(nz)

	def line_pos(self, x):
		b = self.size[1]
		return (-self.slope * x) + b

	def line_neg(self, x):
		return self.slope * x

	def add_gameobject(self, obj):
		self.add_object(obj)
		self.game_objects.append(obj)

	def on_load(self):
		cntr = self.center()
		self.player.move_to(*cntr)
		self.playerhb.move_to(cntr[0]-(self.playerhb.width/2.0), cntr[1])
		self.slope = self.size[1]/float(self.size[0])

		spawn = (251, 244)
		self.cam_x = (spawn[0] * self.tilesize) - (self.size[0]/2)
		self.cam_y = (spawn[1] * self.tilesize) - (self.size[1]/2)

		self.kiddo.move_to(spawn[0] * self.tilesize, spawn[1] * self.tilesize)

	def logic(self):
		self.shoot_cooldown.frame()

	# Manual draw function
	def _draw(self):
		if not self.paused:
			self.game.screen.fill(self.background)

			drawbuffer = 1
			x_wid = math.ceil(self.size[0] / self.tilesize)
			y_wid = math.ceil(self.size[1] / self.tilesize)
			cam_gx = math.floor(self.cam_x / self.tilesize)
			cam_gy = math.floor(self.cam_y / self.tilesize)
			x_range = xrange(int(cam_gx-drawbuffer), int(cam_gx+x_wid)+drawbuffer)
			y_range = xrange(int(cam_gy-drawbuffer), int(cam_gy+y_wid)+drawbuffer)

			for x in x_range:
				for y in y_range:
					try:
						obj = self.grid[x, y]
						obj.x = (x * self.tilesize) - self.cam_x
						obj.y = (y * self.tilesize) - self.cam_y
						obj.draw()
					except KeyError:
						pass

			for obj in self.game_objects:
				if obj.enabled:
					obj.x = obj.game_x - self.cam_x
					obj.y = obj.game_y - self.cam_y
					obj.draw()

			for fixture, posn in self.fixtures:
				fixture.draw(self, posn)

			for obj in self.objects:
				obj._draw()

			self.draw()

	def control(self, buttons, mousepos):
		if not self.paused:
			mouseX, mouseY = mousepos
			key_input = False
			deltaX = 0
			deltaY = 0

			if buttons[stellar.keys.S_HELD][resources.CONTROL_UP]:
				deltaY -= self.move_speed
				key_input = True
			if buttons[stellar.keys.S_HELD][resources.CONTROL_DOWN]:
				deltaY += self.move_speed
				key_input = True
			if buttons[stellar.keys.S_HELD][resources.CONTROL_LEFT]:
				deltaX -= self.move_speed
				key_input = True
			if buttons[stellar.keys.S_HELD][resources.CONTROL_RIGHT]:
				deltaX += self.move_speed
				key_input = True

			# if buttons[stellar.keys.S_PUSHED][stellar.keys.K_ESCAPE]:
			# 	self.pause()

			if buttons[stellar.keys.S_PUSHED][stellar.keys.M_1] and self.shoot_cooldown.is_done():
				self.shoot_cooldown.reset()
				random.choice(resources.GUN_SHOTS).play()
				x = self.cam_x + (self.size[0]/2)
				y = self.cam_y + (self.size[1]/2)
				targetX = mouseX + self.cam_x
				targetY = mouseY + self.cam_y
				bullet = Bullet(x, y, (targetX, targetY))
				self.bullets.append(bullet)
				self.add_gameobject(bullet)

				deltaX -= bullet.ostepx*2
				deltaY -= bullet.ostepy*2

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

			self.player.moving = bool(self.player.direction) and key_input

			deltaX, deltaY = self.playerhb.check_valid(deltaX, deltaY)

			pos = self.line_pos(mouseX) > mouseY
			neg = self.line_neg(mouseX) > mouseY

			if self.player.backwards:
				self.move_speed = self.slowed_speed
			else:
				self.move_speed = self.max_speed

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
		else:
			self.menu_step(buttons, mousepos)

	def draw(self):
		if self.game.debug:
			self.draw_text("%s, %s" % self.game.mousepos, (10, 10), resources.FONT_ARIAL_WHITE_12)
			self.draw_text("%sFPS" % self.game.clock.get_fps(), (10, 30), resources.FONT_ARIAL_WHITE_12)
			self.draw_rect((255, 255, 255), list(self.center()) + [3, 3])
