import stellar
import room_menu
import room_game

class Game(stellar.base.Base):
	def __init__(self):
		stellar.base.Base.__init__(self)
		self.title = "The Man With No Nametag"

		self.add_room("room_menu", room_menu.Room())
		self.add_room("room_game", room_game.Room())

		self.set_room("room_menu")

	def logic(self):
		print self.clock.get_fps()

	# Called by the menu buttons when 'start' is pressed
	def start_game(self):
		self.set_room("room_game")

game = Game()
game.start()