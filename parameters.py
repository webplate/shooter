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
SPREADER0_0 = {'name':'spreader_0',
'type' : 'Bullet',
'trajectory' : 'Up',
'speed' : 0.3,
'cooldown' : 100,
'collision_type' : 'pixel_perfect'
}

SPREADER0_22_5 = {'name':'spreader_0_22.5',
'type' : 'Bullet',
'trajectory' : 'Line',
'trajectory_params' : {'angle' : 22.5},
'speed' : SPREADER0_0['speed'],
'cooldown' : SPREADER0_0['cooldown'],
'collision_type' : 'pixel_perfect'
}

SPREADER0_MINUS22_5 = {'name':'spreader_0_-22.5',
'type' : 'Bullet',
'trajectory' : 'Line',
'trajectory_params' : {'angle' : -22.5},
'speed' : SPREADER0_0['speed'],
'cooldown' : SPREADER0_0['cooldown'],
'collision_type' : 'pixel_perfect'
}

SPREADER0_45 = {'name':'spreader_0_45',
'type' : 'Bullet',
'trajectory' : 'Line',
'trajectory_params' : {'angle' : 45},
'speed' : SPREADER0_0['speed'],
'cooldown' : SPREADER0_0['cooldown'],
'collision_type' : 'pixel_perfect'
}

SPREADER0_MINUS45 = {'name':'spreader_0_-45',
'type' : 'Bullet',
'trajectory' : 'Line',
'trajectory_params' : {'angle' : -45},
'speed' : SPREADER0_0['speed'],
'cooldown' : SPREADER0_0['cooldown'],
'collision_type' : 'pixel_perfect'
}

BULLET = {'name':'o',
'type' : 'Bullet',
'trajectory' : 'Down',
'speed' : 0.15,
'cooldown' : SPREADER0_0['cooldown'] * 6,
'collision_type' : 'pixel'
}

BLAST = {'name' : 'blast',
'type' : 'Blast',
'trajectory' : 'Up',
'speed' : 0.2,
'cooldown' : SPREADER0_0['cooldown'] * 6,
'power': -1,
'collision_type' : 'rectangle'
}

#weapons
#################################
SPREADER0 = {'name' : 'spreader0',
'levels' : [[SPREADER0_0],[SPREADER0_MINUS22_5, SPREADER0_0, SPREADER0_22_5],
[SPREADER0_MINUS45, SPREADER0_MINUS22_5, SPREADER0_0, SPREADER0_22_5, SPREADER0_45]]
}

BLASTER = {'level0' : [BLAST]
}

CANON = {'level0' : [BULLET]
}

#entities
#################################
SHIP = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : 0.2,
'charge_rate' : 0.001,
'life' : 10,
'weapons' : [SPREADER0_0, BLAST]
}

INVINCIBLE = {'name' : 'ship',
'type' : 'Ship',
'ally' : True,
'speed' : 0.2,
'charge_rate' : 0.001,
'life' : 10000,
'weapons' : [SPREADER0_0, BLAST]
}

SAUCER = {'name':'target',
'type' : 'Fighter',
'speed': 0.05,
'life': 5,
'weapons' : [BULLET],
'trajectory' : 'Circular',
'reward' : 1,
'bonus_rate' : 1
}

DESERT = {'name':'desert',
'type' : 'Landscape',
'speed': 0.04,
'layer' : 0
}

DEFAULTBACKGROUND = {'name':'background',
'type' : 'Landscape',
'speed': 0.04,
'layer' : 0
}

BONUSLIFE = {'name' : 'bonusL',
'type' : 'Mobile',
'speed' : 0.1,
'trajectory' : 'OscillationDown',
'trajectory_params' : {'amplitude' : 2},
'collision_type' : 'pixel_perfect',
'effect' : {'add_life' : 1}
}

BONUSWEAPON = {'name' : 'bonusW',
'type' : 'Mobile',
'speed' : 0.1,
'trajectory' : 'OscillationDown',
'trajectory_params' : {'amplitude' : 2},
'collision_type' : 'pixel_perfect',
'effect' : {'upgrade_weapon' : 1},
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
