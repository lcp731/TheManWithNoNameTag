import stellar
import resources

class Room(stellar.rooms.Room):
	def __init__(self):
		stellar.rooms.Room.__init__(self)

		spr_start_default = stellar.sprites.Compound(
			stellar.sprites.Box((120, 0, 0), 180, 50),
			stellar.sprites.Text("Start", resources.FONT_ARIAL_WHITE_30, xoffset=5, yoffset=5)
		)
		spr_start_hover = stellar.sprites.Compound(
			stellar.sprites.Box((180, 0, 0), 180, 50),
			stellar.sprites.Text("Start", resources.FONT_ARIAL_WHITE_30, xoffset=5, yoffset=5)
		)
		spr_start_down = stellar.sprites.Compound(
			stellar.sprites.Box((250, 0, 0), 180, 50),
			stellar.sprites.Text("Start", resources.FONT_ARIAL_WHITE_30, xoffset=5, yoffset=5)
		)

		self.btn_start = stellar.objects.Button(spr_start_default, spr_start_hover, spr_start_down)
		self.btn_start.when_clicked(self.start_game)
		self.btn_start.move_to(10, 10)

		self.add_object(self.btn_start)

	def start_game(self):
		self.game.start_game()