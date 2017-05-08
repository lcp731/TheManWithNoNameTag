import stellar
import tools

stellar.log("Loading resources")

TILESIZE = 64

FONT_ARIAL_WHITE_30 = stellar.tools.Font("resources/fonts/arial.ttf", 30, (255, 255, 255))
FONT_WESTERN_WHITE_30 = stellar.tools.Font("resources/fonts/Pixel-Western.ttf", 30, (255, 255, 255))

AUDIO_ZOMBIE_HIT_SQUAD = stellar.sound.Music("resources/audio/Zombie_Hit_Squad.mp3")
AUDIO_GUNSHOT = stellar.sound.Effect("resources/audio/GUN-Shot.wav")
AUDIO_HOVER_CLICK = stellar.sound.Effect("resources/audio/click.wav")
AUDIO_PRESS_CLICK = stellar.sound.Effect("resources/audio/click4.wav")

LEVEL_TEST = tools.parse_level("resources/levels/beersy.lvl")

IMGS = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/spritesheet.png"),
	(0, 0, 64, 64),
	(64, 0, 64, 64),
	(128, 0, 64, 64),
	(192, 0, 64, 64),
	(256, 0, 64, 64),
	(320, 0, 64, 64),
	(384, 0, 64, 64),
	(448, 0, 64, 64),
	(512, 0, 64, 64),
	(576, 0, 64, 64)
)

_TILE_POINTS = []
for x, y in tools.itergrid(12, 12):
	_TILE_POINTS.append((x*32, y*32, 32, 32))

_LEFTY_POINTS = []
for y, x in tools.itergrid(4, 9):
	_LEFTY_POINTS.append((x*42, y*56, 42, 56))

_LEFTY = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/lefty.png", transparent_bkg=True),
	*_LEFTY_POINTS
)

_TILESET = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/tileset.png"),
	*_TILE_POINTS
)

stellar.tools.transform_sprites(_LEFTY, 2.0)
stellar.tools.transform_sprites(_TILESET, TILESIZE/32.0)

TILE_REFERENCE = {}
for posn, tile in zip(tools.itergrid(12, 12), _TILESET):
	TILE_REFERENCE[posn] = tile

LEFTY_STAND_FORWARD = [_LEFTY[8], _LEFTY[17]]
LEFTY_STAND_BACKWARD = [_LEFTY[26], _LEFTY[34]]