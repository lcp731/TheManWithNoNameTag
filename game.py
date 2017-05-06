import stellar
import room_menu
import room_game

class Game(stellar.base.Base):
	def __init__(self):
		stellar.base.Base.__init__(self)
		self.title = "The Man With No Nametag"
		self.size = (1000, 700)

		self.add_room("room_menu", room_menu.Room())
		self.add_room("room_game", room_game.Room())

		self.set_room("room_menu")

	# Called by the menu buttons when 'start' is pressed
	def start_game(self):
		stellar.log("Start pressed")
		self.set_room("room_game")

game = Game()
game.start()