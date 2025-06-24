
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
TILESIZE = 32
TILESIZE_Texture = 64
FPS = 60

# Layers
BOSS_LAYER = 5
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 2
ENEMY_SPEED = 1

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

BG_COLOR = (50, 50, 80)
COLOR_INACTIVE = (100, 100, 100)
COLOR_ACTIVE = (255, 255, 255)
COLOR_BUTTON = (70, 70, 120)

# Fonts
FONT_SIZE = 32
BIG_FONT_SIZE = 48
FONT = None 
BIG_FONT = None  

# Updated tilemap with enemy types
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BGGGGGGGGGGGLLLLLLLLLLGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGLLWWWLLLLLLLLLLL..................................................................B',
    'BLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWW................TTTTTT...........E...........................................B',
    'B.....................R..LLLLLLLLGGGGGGLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLWWW..............L.TTLLLT..........E............................................B',
    'B.............K..........TTKLLLLLLGGGGGLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLWWW..............L.TTGGGT.........E.............................................B',
    'B.....................E.LTTGGGGGGGGGGGGGGGGGGGGGGLTTTTTTTTTTTTTTTTTTTTTTMMM.............L.TTTGGGT.......................................................B',
    'B.......................LTTGGGLLLLLLLLLLLLLLLLLLLLLLTTTTTTTTTTTTTTTTTTTTMMM.............L.TTTGGGT...........R...........................................B',
    'B.....E.................LTTGGGGGGGGGGGGGGGGGGGGGGGLTTLLLLLLLLLLLLLLLLLLLWWW.............L.TTTGGGT........R..............................................B',
    'B.....E.................LTTGGGLLLLLLLLLLKLLLLLLLLLLTTL..................WWW.............L.TTTGGGT......K................................................B',
    'B.....E.................LTTGGGGGGGGGGGGGGGGGGGGGGGLTTL..................WWW.............L.TTTGGGT......K................................................B',
    'B.....E.................LTTGGGLLLLLLLLLLLLLLLLLLLLLTTL.............E....WWW.............L.TTTGGGT.......................................................B',
    'B.....R.................LTTGGGTGGGGGGGGGGGGGGGGGGGLTTL..............E...WWW.............L.TTTGGGT.......................................................B',
    'B.....K.......E.........LTTGGGLLLLLLLLLLLLLLLLLLLLLTTL..............E...WWW.............L.TTRGGGT.......................................................B',
    'B..............R........LTTGGGGGGGGGGGGGGGGGGGGGGGLTTL..............R...WWW.............L.TTEGGGT...........................................Y...........B',
    'B...............K.......LTTLLLLLLLLLLLLLLLLLLLLLLLLTTL................K.WWW.............LTTTKLLLT.......................................................B',
    'BTTTTTTTTTTTTTETTTTTTTTTTTPTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMMMTTTTTTTTTTTTTTTTTTLLLT........................................................B',
    'BTTTTTTTTTTTTTTTTTTETTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTMMMTTTTTTTTTTTTTTTTTTLLLT...............................................Y........B',
    'BGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWWWWWGGGGGGGGGGGGGGGGGGGG...............................................Y.......B',
    'BLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLWWWWWWWLLLLLLLLLLLLLLLLLLL............................................Y.......B',
    'B.GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWWWWWW................................................................X.......B',
    'BLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLWWWWWWWWW............................................................Y........B',
    'BGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWWWWWWWWWW.........................................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
# Враги:
# E - обычный враг
# R - дальнобойный (ranged)
# K - танк
#GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
#LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL