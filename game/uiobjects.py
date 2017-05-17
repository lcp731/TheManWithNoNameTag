import stellar
import pygame
import resources
import math

def cos(deg):
	return math.cos(math.radians(deg))

def sin(deg):
	return math.sin(math.radians(deg))

class GreyOut(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)

		self.add_sprite("blank", stellar.sprites.Sprite())
		self.set_sprite("blank")

		self.surf = pygame.Surface(resources.GAME_SIZE, pygame.SRCALPHA, 32)
		self.surf.fill((0, 0, 0, 10))

	def _draw(self):
		self.room.draw_blit(self.surf, (0,0))

class Bullet(stellar.objects.Object):
	ANGLE = 60
	RADIUS = 50
	OFFSET = 0

	def __init__(self, num):
		stellar.objects.Object.__init__(self)
		self.num = num
		self.rest_angle = self.ANGLE * self.num

		self.add_sprite("full", stellar.sprites.Ellipse((255, 0, 0), 10, 10))
		self.add_sprite("empty", stellar.sprites.Ellipse((50, 0, 0), 10, 10))
		self.add_sprite("blocked", stellar.sprites.Ellipse((100, 0, 0), 10, 10))
		self.set_sprite("full")

		# if not num:
		# 	self.set_sprite("blocked")

	def update_angle(self):
		self.x = cos(self.rest_angle + self.OFFSET - 90) * self.RADIUS
		self.y = sin(self.rest_angle + self.OFFSET - 90) * self.RADIUS

		self.x += self.mid_x
		self.y += self.mid_y

	def move_to(self, x, y):
		self.mid_x = x
		self.mid_y = y

		self.update_angle()

	def logic(self):
		self.update_angle()

class Revolver(stellar.objects.Object):
	def __init__(self, *bullets):
		stellar.objects.Object.__init__(self)

		self.add_sprite("default", stellar.sprites.Sprite())
		self.set_sprite("default")

		self.bullets = bullets
		self.bullet = 0

		self.to_move = 0
		self.move_speed = 2

	def move_to(self, x, y):
		self.x = x
		self.y = y
		for b in self.bullets:
			b.move_to(x, y)

	def room_link(self, room):
		self.room = room
		for b in self.bullets:
			self.room.add_object(b)

	def control(self, buttons, mousepos):

		if buttons[stellar.keys.S_PUSHED][stellar.keys.K_SPACE]:
			self.to_move = Bullet.ANGLE
			self.bullets[self.bullet].set_sprite("empty")
			self.bullet += 1

	def logic(self):
		if self.to_move > 0:
			Bullet.OFFSET += self.move_speed
			self.to_move -= self.move_speed

# testgame = stellar.base.Base()
# mainroom = stellar.rooms.Room()

# revolver = Revolver(
# 	Bullet(0),
# 	Bullet(1),
# 	Bullet(2),
# 	Bullet(3),
# 	Bullet(4),
# 	Bullet(5)
# )

# revolver.move_to(100, 100)

# mainroom.add_object(revolver)
# testgame.add_room("mainroom", mainroom)
# testgame.set_room("mainroom")
# testgame.start()