
WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
FPS = 60
#player layer meaning that it ill be a layer above the blocks
PLAYER_LAYER = 5
ENEMY_LAYER = 4
HEALTH_BAR_LAYER = 6
UI_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GREY = (128,128,128)
GREEN = (0,128,0)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBB         BBBBBBBBBBBBBBBBBBBB',            
    'B..................B         B..................B',   
    'B..................B         B.........E........B',
    'B....E.............B         B..................B',
    'B..................B         B..................B',
    'B..................BBBBBBBBBBB..................B',
    'B...............................................B',
    'B........P......................................B',
    'B..................BBBBBBBBBBB..................B',
    'B..................B         B..................B',
    'B..................B         B..................B',
    'B..................B         B...E..............B',
    'B..............E...B         B..............E...B',
    'B..................B         B..................B',
    'BBBBBBBBBBBBBBBBBBBB         BBBBBBBBBBBBBBBBBBBB',
]

battle_map = [
'BBBBBBBBBBBBBBBBBBBB',
'B..................B',
'B..................B',
'B....P.......E.....B',
'B..................B',
'B..................B',
'BBBBBBBBBBBBBBBBBBBB',

]

