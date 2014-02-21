#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *

GAMESIZE = (320, 240) #~neo geo
COLORDEPTH = 16 #set to 8 for speedier game with low color resolution !
RESCALE = '2x' #set to 2x or mame

fullscreen_key = K_f
#control settings
R_key = K_RIGHT
L_key = K_LEFT
U_key = K_UP
D_key = K_DOWN
Shoot_key = K_SPACE

DEFAULTPLAY = {'name':'default',
'flash_pulse': 16,     #ms
'hit_pulse' : 100,
'speed' : 0.2,     #px/ms
'bullet_speed': 0.4
}

SLOWMO = {'name':'default',
'flash_pulse': 500,     #ms
'hit_pulse' : 100,
'speed' : 0.2,     #px/ms
'bullet_speed': 0.02
}

GAMEPLAY = DEFAULTPLAY

#Theme packs
TXTTHEME = {'name' : None,
'explosion_pulse' : 100,
'bg_color' : (50, 50, 50),
'txt_color' : (200, 200, 200),
'font' : "./fonts/Fipps-Regular.otf",
'txt_size' : 8,
'txt_inter' : 8
}

DERVAL = {'name':'derval',
'explosion_pulse' : 100,
'bg_color' : (50, 50, 100),
'txt_color' : (200, 200, 200),
'font' : "./fonts/Fipps-Regular.otf",
'txt_size' : 8,
'txt_inter' : 8
}

IRONBRAIN = {'name':'ironbrain',
'explosion_pulse' : 100,
'bg_color' : (100, 150, 100),
'txt_color' : (200, 200, 200),
'font' : "./fonts/Fipps-Regular.otf",
'txt_size' : 8,
'txt_inter' : 8
}

#projectiles
BULLET = {'name':'A',
'type' : 'Bullet',
'direction' : 'up',
'speed' : GAMEPLAY['bullet_speed'],
'cooldown' : 100,
'damage' : 1
}

BULLET2 = {'name':'o',
'type' : 'Bullet',
'direction' : 'down',
'speed' : GAMEPLAY['bullet_speed'],
'cooldown' : BULLET['cooldown'] * 6,
'damage' : 1,
}

BLAST = {'name' : 'oOOo',
'type' : 'Blast',
'direction' : 'up',
'speed' : GAMEPLAY['bullet_speed'],
'cooldown' : BULLET['cooldown'] * 6,
'power': 3,
}

#entities
SHIP = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : GAMEPLAY['speed'],
'charge_rate' : 0.001,
'life' : 10,
'weapons' : [BULLET, BLAST]
}

INVINCIBLE = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : GAMEPLAY['speed'],
'charge_rate' : 0.001,
'life' : 100,
'weapons' : [BULLET, BLAST]
}

TARGET = {'name':'target',
'type' : 'Fighter',
'speed':GAMEPLAY['speed'] / 2,
'life': 5,
'weapons' : [BULLET2]
}

#The reference playable level used to complete others
DEFAULTLEVEL = {'name':'default',
'theme' : TXTTHEME,
'gameplay' : GAMEPLAY,
'content' : [SHIP],
'nb_enemies' : 3
}

LEVELSLOW = {'name':'slowmo',
'theme' : TXTTHEME,
'gameplay' : SLOWMO,
'nb_enemies' : 3
}

LEVELSTRESS = {'name':'stress',
'theme' : DERVAL,
'nb_enemies' : 50,
'content' : [INVINCIBLE]
}

LEVEL = LEVELSTRESS
