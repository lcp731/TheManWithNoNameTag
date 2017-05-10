import stellar
import tools

stellar.log("Loading resources")

TILESIZE = 64

CONTROL_UP = stellar.keys.K_w
CONTROL_DOWN = stellar.keys.K_s
CONTROL_LEFT = stellar.keys.K_a
CONTROL_RIGHT = stellar.keys.K_d

FONT_ARIAL_WHITE_30 = stellar.tools.Font("resources/fonts/arial.ttf", 30, (255, 255, 255))
FONT_ARIAL_WHITE_12 = stellar.tools.Font("resources/fonts/arial.ttf", 12, (255, 255, 255))
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

_LEFTY_STAND = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/leftystand.png", transparent_bkg=True),
	(0, 0, 42, 56),
	(42, 0, 42, 56),
	(84, 0, 42, 56),
	(126, 0, 42, 56)
)

_TILE_POINTS = []
for x, y in tools.itergrid(12, 12):
	_TILE_POINTS.append((x*32, y*32, 32, 32))

_LEFTY_POINTS = []
for y, x in tools.itergrid(8, 9):
	_LEFTY_POINTS.append((x*42, y*56, 42, 56))

_LEFTY = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/newlefty.png", transparent_bkg=True),
	*_LEFTY_POINTS
)

_TILESET = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/tileset.png"),
	*_TILE_POINTS
)

stellar.tools.transform_sprites(_LEFTY, 2.0)
stellar.tools.transform_sprites(_LEFTY_STAND, 2.0)
stellar.tools.transform_sprites(_TILESET, TILESIZE/32.0)

TILE_REFERENCE = {}
for posn, tile in zip(tools.itergrid(12, 12), _TILESET):
	TILE_REFERENCE[posn] = tile

# LEFTY_ARM_DOWN = stellar.sprites.Image("resources/images/leftyarm/down.png").perma_scale(2.0)
# LEFTY_ARM_DOWNLEFT = stellar.sprites.Image("resources/images/leftyarm/downleft.png").perma_scale(2.0)
# LEFTY_ARM_DOWNRIGHT = stellar.sprites.Image("resources/images/leftyarm/downright.png").perma_scale(2.0)
# LEFTY_ARM_LEFT = stellar.sprites.Image("resources/images/leftyarm/left.png").perma_scale(2.0)
# LEFTY_ARM_RIGHT = stellar.sprites.Image("resources/images/leftyarm/right.png").perma_scale(2.0)
# LEFTY_ARM_UP = stellar.sprites.Image("resources/images/leftyarm/up.png").perma_scale(2.0)
# LEFTY_ARM_UPLEFT = stellar.sprites.Image("resources/images/leftyarm/upleft.png").perma_scale(2.0)
# LEFTY_ARM_UPRIGHT = stellar.sprites.Image("resources/images/leftyarm/upright.png").perma_scale(2.0)
LEFTY_ARM_LEFT = stellar.sprites.Image("resources/images/arm_left.png").perma_scale(1.7)
LEFTY_ARM_RIGHT = stellar.sprites.Image("resources/images/arm_right.png").perma_scale(1.7)


LEFTY_STAND_FORWARD_NOGUN_L = [_LEFTY[8], _LEFTY[17]]
LEFTY_STAND_BACKWARD_NOGUN_L = [_LEFTY[26], _LEFTY[35]]

LEFTY_STAND_FORWARD_NOGUN_R = [tools.clone(_LEFTY[8]).flip(True, False), tools.clone(_LEFTY[17]).flip(True, False)]
LEFTY_STAND_BACKWARD_NOGUN_R = [tools.clone(_LEFTY[26]).flip(True, False), tools.clone(_LEFTY[35]).flip(True, False)]

LEFTY_STAND_FORWARD_L = [_LEFTY_STAND[0]]
LEFTY_STAND_FORWARD_R = [_LEFTY_STAND[1]]

LEFTY_STAND_BACKWARD_L = [_LEFTY_STAND[2]]
LEFTY_STAND_BACKWARD_R = [_LEFTY_STAND[3]]

LEFTY_RUN_FL = _LEFTY[0:8]
LEFTY_RUN_FR = _LEFTY[9:17]
LEFTY_RUN_BL = _LEFTY[18:26]
LEFTY_RUN_BR = _LEFTY[27:35]
LEFTY_BACK_FL = _LEFTY[36:44]
LEFTY_BACK_FR = _LEFTY[45:53]
LEFTY_BACK_BL = _LEFTY[54:62]
LEFTY_BACK_BR = _LEFTY[63:71]