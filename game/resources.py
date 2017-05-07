import stellar

stellar.log("Loading resources")

FONT_ARIAL_WHITE_30 = stellar.tools.Font("resources/fonts/arial.ttf", 30, (255, 255, 255))
FONT_WESTERN_WHITE_30 = stellar.tools.Font("resources/fonts/Pixel-Western.ttf", 30, (255, 255, 255))

AUDIO_ZOMBIE_HIT_SQUAD = stellar.sound.Music("resources/audio/Zombie_Hit_Squad.mp3")
AUDIO_GUNSHOT = stellar.sound.Effect("resources/audio/GUN-Shot.wav")
AUDIO_HOVER_CLICK = stellar.sound.Effect("resources/audio/click.wav")
AUDIO_PRESS_CLICK = stellar.sound.Effect("resources/audio/click4.wav")

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

_TILESET = stellar.tools.load_sheet(
	stellar.sprites.Image("resources/images/tileset.png"),
	(128, 160, 32, 32),
	(160, 160, 32, 32),
	(192, 160, 32, 32),
	(224, 160, 32, 32),
	(256, 160, 32, 32),
	(288, 160, 32, 32),
	(320, 160, 32, 32),
	(352, 160, 32, 32),
	(128, 192, 32, 32),
	(160, 192, 32, 32),
	(192, 192, 32, 32),
	(224, 192, 32, 32),
	(256, 192, 32, 32),
	(288, 192, 32, 32),
	(320, 192, 32, 32),
	(352, 192, 32, 32),
	(128, 224, 32, 32),
	(160, 224, 32, 32),
	(192, 224, 32, 32),
	(224, 224, 32, 32),
	(256, 224, 32, 32),
	(288, 224, 32, 32),
	(320, 224, 32, 32),
	(352, 224, 32, 32),
	(128, 256, 32, 32),
	(160, 256, 32, 32),
	(192, 256, 32, 32),
	(224, 256, 32, 32),
	(256, 256, 32, 32),
	(288, 256, 32, 32),
	(320, 256, 32, 32),
	(352, 256, 32, 32),
)

stellar.tools.transform_sprites(_TILESET, 2.0)

TILE_TL0_64 = _TILESET[0]
TILE_TL1_64 = _TILESET[2]
TILE_TL2_64 = _TILESET[4]
TILE_TL3_64 = _TILESET[6]
TILE_TL4_64 = _TILESET[16]
TILE_TL5_64 = _TILESET[18]
TILE_TL6_64 = _TILESET[20]
TILE_TL7_64 = _TILESET[22]

TILE_TR0_64 = _TILESET[1]
TILE_TR1_64 = _TILESET[3]
TILE_TR2_64 = _TILESET[5]
TILE_TR3_64 = _TILESET[7]
TILE_TR4_64 = _TILESET[17]
TILE_TR5_64 = _TILESET[19]
TILE_TR6_64 = _TILESET[21]
TILE_TR7_64 = _TILESET[23]

TILE_BL0_64 = _TILESET[8]
TILE_BL1_64 = _TILESET[10]
TILE_BL2_64 = _TILESET[12]
TILE_BL3_64 = _TILESET[14]
TILE_BL4_64 = _TILESET[24]
TILE_BL5_64 = _TILESET[26]
TILE_BL6_64 = _TILESET[28]
TILE_BL7_64 = _TILESET[30]

TILE_BR0_64 = _TILESET[9]
TILE_BR1_64 = _TILESET[11]
TILE_BR2_64 = _TILESET[13]
TILE_BR3_64 = _TILESET[15]
TILE_BR4_64 = _TILESET[25]
TILE_BR5_64 = _TILESET[27]
TILE_BR6_64 = _TILESET[29]
TILE_BR7_64 = _TILESET[31]