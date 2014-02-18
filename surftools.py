#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pygame
from parameters import *

def get_center(pos, surface) :
    center = (pos[0]+surface.get_width()/2, pos[1]+surface.get_height()/2)
    return center

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join('imgs', file, '.png')
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    surface.convert_alpha()
    return surface

def make_array(surface) :
    return pygame.surfarray.array2d(surface).astype(bool)

def font_skin(font, name) :
    """if no pics create from font"""
    surface = font.render(name, False, txt_color)
    return surface

