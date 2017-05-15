import time
import stellar
import resources
import room_menu
import room_game

class Game(stellar.base.Base):
	def __init__(self):
		stellar.base.Base.__init__(self)
		self.title = "The Man With No Nametag"
		self.size = (1300, 800)

		self.debug = True

		self.target_framerate = 60

		self.add_room("room_menu", room_menu.Room())
		self.add_room("room_game", room_game.Room())

		self.set_room("room_menu")

		stellar.log("Game initialised")

	def on_start(self):
		stellar.log("Game started")

	def on_stop(self):
		stellar.log("Game stopped")

	# Called by the menu buttons when 'start' is pressed
	def start_game(self):
		stellar.log("Start button pressed")
		# stellar.log("Starting music")
		# resources.AUDIO_ZOMBIE_HIT_SQUAD.play()
		# resources.AUDIO_ZOMBIE_HIT_SQUAD.set_volume(0.2)
		self.set_room("room_game")

game = Game()
game.start()
