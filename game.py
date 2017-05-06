import stellar
import room_menu

class Game(stellar.base.Base):
	def __init__(self):
		stellar.base.Base.__init__(self)
		self.title = "The Man With No Nametag"

		self.add_room("room_menu", room_menu.Room())

		self.set_room("room_menu")

game = Game()
game.start()