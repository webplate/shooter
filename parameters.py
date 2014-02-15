#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *

#screen settings
full_screen = False
window_size = (640, 480)


#interface style
bg_color = (0, 0, 0)
txt_color = (100, 100, 100)
txt_font = "./fonts/Fipps-Regular.otf"
txt_size = 16
txt_inter = txt_size + 2


#control settings
R_key = K_RIGHT
L_key = K_LEFT
U_key = K_UP
D_key = K_DOWN
Shoot_key = K_SPACE

#physics tuning
BASE_POWER = 0.1
BULLET_SPEED = 0.3
BASE_COOLDOWN = 500
SHIP_COOLDOWN = 100
