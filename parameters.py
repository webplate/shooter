#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l

GAMESIZE = (320, 240) #~neo geo
#~ GAMESIZE = (1024, 500)
COLORDEPTH = 16 #set to 8 for speedier game with low color resolution !
RESCALE = '2x' #set to 2x or mame

#control settings
KEYMAP1 = {p_l.K_f : 'fullscreen',
p_l.K_p : 'pause',
p_l.K_RIGHT : 'right',
p_l.K_LEFT : 'left',
p_l.K_UP : 'up',
p_l.K_DOWN : 'down',
p_l.K_SPACE : 'shoot'
}

KEYMAP2 = {p_l.K_d : 'right',
p_l.K_q : 'left',
p_l.K_z : 'up',
p_l.K_s : 'down',
p_l.K_LSHIFT : 'shoot'
}

KEYMAPS = [KEYMAP1, KEYMAP2]


DEFAULTPLAY = {'name':'default',
'flash_pulse': 16,     #ms
'hit_pulse' : 100,
'speed' : 0.2,     #px/ms
'bullet_speed': 0.25
}

SLOWMO = {'name':'slow',
'flash_pulse': 500,     #ms
'hit_pulse' : 100,
'speed' : 0.1,     #px/ms
'bullet_speed': 0.02
}

GAMEPLAY = DEFAULTPLAY

#Theme packs
DEFAULTTHEME = {'name' : None,
'explosion_pulse' : 100,
'bg_color' : (50, 50, 50),
'txt_color' : (200, 200, 200),
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
'power': 3,
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
'nb_enemies' : 20
}

LEVEL = STRESSLEVEL
