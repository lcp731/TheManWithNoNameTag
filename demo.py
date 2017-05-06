import stellar

class Player(stellar.objects.Object):
	def __init__(self):
		stellar.objects.Object.__init__(self)

		self.add_sprite("default",
			stellar.sprites.Box((255, 0, 0), 20, 20)
		)

		self.set_sprite("default")

	def logic(self):
		pass

	def control(self, buttons, mouse):
		pass

	def draw(self):
		pass

	def on_click(self):
		pass

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		self.player = Player()
		self.player.move_to(20, 20)
		self.add_object(self.player)

game = stellar.base.Base()
game.add_room("main", Room())
game.set_room("main")
game.start()