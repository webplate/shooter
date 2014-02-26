#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l

GAMESIZE = (320, 240) #~neo geo
#~ GAMESIZE = (1024, 500)
COLORDEPTH = 16 #set to 8 for speedier game with low color resolution !
RESCALE = '2x' #set to 2x or mame

#control settings keyed by scancode of pressed key
KEYMAP1 = {41 : 'fullscreen',
33 : 'pause',
114 : 'right',
113 : 'left',
111 : 'up',
116 : 'down',
65 : 'shoot'
}

KEYMAP2 = {40 : 'right',
38 : 'left',
25 : 'up',
39 : 'down',
50 : 'shoot'
}

KEYMAPS = [KEYMAP1, KEYMAP2]


DEFAULTPLAY = {'name':'default',
'flash_pulse': 16,     #ms
'hit_pulse' : 50,
'blast_hit_pulse' : 100,
'game_speed' : 0.5,
'speed' : 0.2,     #px/ms
'bullet_speed': 0.25
}

GAMEPLAY = DEFAULTPLAY

#Theme packs
DEFAULTTHEME = {'name' : None,
'explosion_pulse' : 100,
'bg_color' : (50, 50, 50),
'txt_color' : (100, 100, 100),
'font' : "./fonts/FIXED_BO.TTF",
'monospace_font' : "./fonts/FIXED_BO.TTF",
'small_font' : "./fonts/MiniPower.ttf",
'txt_size' : 8,
'txt_inter' : 8,
'small_size' : 16
}

DERVAL = {'name':'derval'
}

IRONBRAIN = {'name':'ironbrain',
'bg_color' : (100, 110, 100),
'font' : "./fonts/AtariSmall.ttf",
'txt_size' : 16,
'txt_inter' : 16
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
'power': 1,
}

#entities
SHIP = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : GAMEPLAY['speed'],
'charge_rate' : 0.001,
'life' : 100,
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
'speed':GAMEPLAY['speed'] / 4,
'life': 5,
'weapons' : [BULLET2],
'trajectory' : 'Circular'
}

TARGETOLD = {'name':'target',
'type' : 'Fighter',
'speed':GAMEPLAY['speed'] / 2,
'life': 5,
'weapons' : [BULLET2],
'trajectory' : 'AlignV'
}

#The reference playable level used to complete others
DEFAULTLEVEL = {'name':'default',
'theme' : DEFAULTTHEME,
'gameplay' : DEFAULTPLAY,
'nb_enemies' : 3
}

STRESSLEVEL = {'name':'stress',
'theme' : DERVAL,
'nb_enemies' : 10
}

LEVEL = STRESSLEVEL
