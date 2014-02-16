#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pygame

def get_center(pos, surface) :
    center = (pos[0]+surface.get_width()/2, pos[1]+surface.get_height()/2)
    return center

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('imgs', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert_alpha()
