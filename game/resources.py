import stellar

stellar.log("Loading resources")

FONT_ARIAL_WHITE_30 = stellar.tools.Font("resources/fonts/arial.ttf", 30, (255, 255, 255))
FONT_WESTERN_WHITE_30 = stellar.tools.Font("resources/fonts/Pixel-Western.ttf", 30, (255, 255, 255))

AUDIO_ZOMBIE_HIT_SQUAD = stellar.sound.Music("resources/audio/Zombie_Hit_Squad.mp3")
AUDIO_GUNSHOT = stellar.sound.Effect("resources/audio/GUN-Shot.wav")
AUDIO_HOVER_CLICK = stellar.sound.Effect("resources/audio/click.wav")
AUDIO_PRESS_CLICK = stellar.sound.Effect("resources/audio/click4.wav")

IMGS = stellar.sprites.LoadSheet(
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

_TILESET = stellar.sprites.LoadSheet(
	stellar.sprites.Image("resources/images/tileset.png"),
	(128, 96, 64, 64),		# Wall
	(128, 160, 64, 64),		# Shelves 1
	(192, 160, 64, 64),		# Shelves 2
	(256, 160, 64, 64),		# Shelves 3
	(320, 160, 64, 64),		# Shelves 4
	(128, 224, 64, 64),		# Shelves 5
	(192, 224, 64, 64),		# Shelves 6
	(256, 224, 64, 64),		# Shelves 7
	(320, 224, 64, 64),		# Shelves 8
)


TILE_WALL_64 = 	_TILESET[0]
TILE_SHELVES1_64 = _TILESET[1]
TILE_SHELVES2_64 = _TILESET[2]
TILE_SHELVES3_64 = _TILESET[3]
TILE_SHELVES4_64 = _TILESET[4]
TILE_SHELVES5_64 = _TILESET[5]
TILE_SHELVES6_64 = _TILESET[6]
TILE_SHELVES7_64 = _TILESET[7]
TILE_SHELVES8_64 = _TILESET[8]

ARRAY_TILE_SHELVES_64 = [
	TILE_SHELVES1_64,
	TILE_SHELVES2_64,
	TILE_SHELVES3_64,
	TILE_SHELVES4_64,
	TILE_SHELVES5_64,
	TILE_SHELVES6_64,
	TILE_SHELVES7_64,
	TILE_SHELVES8_64
]