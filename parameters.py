#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l

GAMESIZE = (320, 240) #~neo geo
#~ GAMESIZE = (1024, 500)
COLORDEPTH = 16 #set to 8 for speedier game with low color resolution !
RESCALE = '2x' #set to 2x or mame

DEFAULTPLAY = {'name':'default',
'flip_rate' : 70, #fps cap
'flash_pulse': 16,     #ms for white flash when collision
'hit_pulse' : 50, #ms between two hits on ship
'blast_hit_pulse' : 20, #ms between two blast hits
'game_speed' : 1,
'speed' : 0.2,     #px/ms
'bullet_speed': 0.25
}

#control settings
KEYMAP1 = {p_l.K_f : 'fullscreen',
p_l.K_m : 'mute',
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


#Theme packs
DEFAULTTHEME = {'name' : None,
'explosion_pulse' : 100,
'bg_color' : (50, 50, 50),
'txt_color' : (100, 100, 100),
'font' : "FIXED_BO.TTF",
'monospace_font' : "FIXED_BO.TTF",
'small_font' : "MiniPower.ttf",
'txt_size' : 8,
'txt_inter' : 8,
'small_size' : 16
}

DEFAULTSNDPACK = {'name' : None,
'music_volume' : 0.3,
'effect_volume' : 0.2
}

MCPACK = {'name' : 'mc'
}

DERVAL = {'name':'derval'
}

CLEBARD = {'name':'clebard',
'txt_color' : (255, 200, 150)
}

IRONBRAIN = {'name':'ironbrain',
'bg_color' : (100, 110, 100),
'font' : "AtariSmall.ttf",
'txt_size' : 16,
'txt_inter' : 16
}

#projectiles
########################################
BULLET = {'name':'spreader_0',
'type' : 'Bullet',
'trajectory' : 'Up',
'speed' : 1,
'cooldown' : 100,
'damage' : 1,
'collision_type' : 'pixel_perfect'
}

BULLET2 = {'name':'o',
'type' : 'Bullet',
'trajectory' : 'Down',
'speed' : 1,
'cooldown' : BULLET['cooldown'] * 6,
'damage' : 1,
'collision_type' : 'pixel'
}

BLAST = {'name' : 'blast',
'type' : 'Blast',
'trajectory' : 'Up',
'speed' : 1,
'cooldown' : BULLET['cooldown'] * 6,
'power': 1,
'collision_type' : 'rectangle'
}

#entities
#################################
SHIP = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : 1,
'charge_rate' : 0.001,
'life' : 10,
'weapons' : [BULLET, BLAST]
}

INVINCIBLE = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : 1,
'charge_rate' : 0.001,
'life' : 10000,
'weapons' : [BULLET, BLAST]
}

SAUCER = {'name':'target',
'type' : 'Fighter',
'speed': 0.25,
'life': 5,
'weapons' : [BULLET2],
'trajectory' : 'Circular',
'reward' : 1,
'bonus_rate' : 0.2
}

DESERT = {'name':'desert',
'type' : 'Landscape',
'speed': 0.2,
'layer' : 0
}

DEFAULTBACKGROUND = {'name':'background',
'type' : 'Landscape',
'speed': 0.2,
'layer' : 0
}

BONUS = {'name':'bonus',
'type' : 'Mobile',
'speed' : 0.5,
'trajectory' : 'OscillationDown',
'trajectory_params' : {'amplitude' : 20},
'collision_type' : 'pixel_perfect'
}
#Player settins
PLAYER = {'name' : 'player1',
'ship' : SHIP
}

ALTPLAYER = {'name' : 'Bloody Barron',
'ship' : INVINCIBLE
}

#The reference playable level used to complete others
##############################################
DEFAULTLEVEL = {'name':'default',
'theme' : DEFAULTTHEME,
'sound_pack' : DEFAULTSNDPACK,
'gameplay' : DEFAULTPLAY,
'background' : DEFAULTBACKGROUND,
'music' : 'background',
'nb_enemies' : 6,
'player' : PLAYER
}

STRESSLEVEL = {'name':'stress',
'theme' : DERVAL,
'sound_pack' : DEFAULTSNDPACK,
'nb_enemies' : 300,
'player' : ALTPLAYER
}

CLEBLEVEL = {'name':'clebard',
'theme' : CLEBARD,
'sound_pack' : MCPACK,
'background' : DESERT,
'nb_enemies' : 4
}

LEVEL = CLEBLEVEL
