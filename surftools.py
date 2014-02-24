#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pygame
import parameters

def get_center(pos, surface) :
    center = (pos[0]+surface.get_width()/2, pos[1]+surface.get_height()/2)
    return center

def load_image(file, theme, scene):
    """loads an image, prepares it for play
    or create a label if image absent"""
    if theme != None :
        path = os.path.join('imgs', theme, file + '.png')
        try:
            surface = pygame.image.load(path)
        except pygame.error:
            #if no corresponding png generate from label
            surface = font_skin(scene, file)
        else :
            #strip of alpha channel for colorkey transparency and notmuch colors
            surface = surface.convert(parameters.COLORDEPTH)
            #first pixel sets transparent color
            color = surface.get_at((0, 0))
            surface.set_colorkey(color)
    else :
        #no themepack : use labels as sprites 
        surface = font_skin(scene, file)
    return surface

def load_background(file, theme, scene):
    if theme != None :
        path = os.path.join('imgs', theme, file + '.png')
        try:
            surface = pygame.image.load(path)
        except pygame.error:
            #if no corresponding png generate from label
            surface = font_skin(scene, ' ')
        else :
            #strip of alpha channel for colorkey transparency and notmuch colors
            surface = surface.convert(parameters.COLORDEPTH)
    else :
        #no themepack : use labels as sprites 
        surface = font_skin(scene, ' ')
    return surface

def make_array(surface) :
    array = pygame.surfarray.array2d(surface)
    colorkey = surface.map_rgb(surface.get_colorkey())
    w, h = array.shape
    for i in range(w) :
        for j in range(h) :
            if array[i, j] != colorkey :
                array[i, j] = True
            else :
                array[i, j] = False
    return array

def make_white(surface) :
    white = (255, 255, 255)
    black = (0, 0, 0)
    covered = make_array(surface)
    surface = pygame.Surface(surface.get_size(), depth = 8)
    surface.set_palette([black, white])
    pix_array = pygame.PixelArray(surface)
    w, h = covered.shape
    for i in range(w) :
        for j in range(h) :
            if covered[i,j] :
                pix_array[i,j] = white
            else :
                pix_array[i,j] = black
    surface.set_colorkey(black)
    return surface

def font_skin(scene, name) :
    """if no pics create from font"""
    surface = scene.font.render(name, False, scene.theme['txt_color'])
    return surface

