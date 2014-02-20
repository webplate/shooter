#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *


GAMESIZE = (320, 240) #~neo geo
COLORDEPTH = 16 #set to 8 for speedier game with low color resolution !
RESCALE = '2x' #set to 2x or mame

#interface style
bg_color = (100, 100, 100)
txt_color = (200, 200, 200)
txt_font = "./fonts/Fipps-Regular.otf"
txt_size = 8
txt_inter = txt_size * 2
THEME = None
USE_PICS = True
HITPULSE = 16 #ms

fullscreen_key = K_f
#control settings
R_key = K_RIGHT
L_key = K_LEFT
U_key = K_UP
D_key = K_DOWN
Shoot_key = K_SPACE

#physics tuning
#ship
BASE_SPEED = 0.2 #px/ms
SHIP_COOLDOWN = 100 #ms
CHARGE_RATE = 0.001
SHIPLIFE = 1000
#enemies
TARGET_SPEED = BASE_SPEED  / 2
BASE_COOLDOWN = SHIP_COOLDOWN * 6
BASELIFE = 5

#projectile
BASEPULSE = 100 #ms
BULLET_SPEED = BASE_SPEED * 2
#~ BULLET_SPEED = BASE_SPEED / 10
BASEDAMAGE = 1
BLASTPOWER = 3
EXPLOSIONPULSE = 100

NBENEMIES = 3




