#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, pygame
import parameters

def get_center(pos, surface) :
    center = (pos[0]+surface.get_width()/2, pos[1]+surface.get_height()/2)
    return center

def load_sound(file, scene) :
    """load sound or not"""
    if scene.snd_pack['name'] != None :
        path = os.path.join('sounds', scene.snd_pack['name'], file + '.ogg')
        try :
            sound = pygame.mixer.Sound(path)
        except pygame.error :
            sound = None
    else :
        sound = None
    return sound

def load_stream(file, scene) :
    """load music track or not"""
    if scene.snd_pack['name'] != None :
        path = os.path.join('sounds', scene.snd_pack['name'], file + '.ogg')
        try :
            sound = pygame.mixer.music.load(path)
        except pygame.error :
            sound = None
    else :
        sound = None
    return sound

def load_image(file, theme, scene):
    """loads an image, prepares it for play
    or create a label if image absent"""
    if theme != None :
        path = os.path.join('imgs', theme, file + '.png')
        try:
            surface = pygame.image.load(path)
        except pygame.error :
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
            #if no corresponding png : empty background
            surface = font_skin(scene, ' ')
        else :
            surface = surface.convert(parameters.COLORDEPTH)
    else :
        #no themepack : empty background
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
    #bypass unfitted one dimensional pixel array if w = 1
    if w != 1 :
        for i in range(w) :
            for j in range(h) :
                if covered[i,j] :
                    pix_array[i,j] = white
                else :
                    pix_array[i,j] = black
    else :
        for i in range(w) :
            for j in range(h) :
                if covered[i,j] :
                    surface.set_at((i, j), white)
                else :
                    surface.set_at((i, j), black)
    surface.set_colorkey(black)
    return surface

def compose_surfaces(s1, s2, w, h):
    """gets two surfaces and blit them on a new one
    of size w,h
    """
    s = pygame.Surface((w, h))
    s.blit(s1, (0, 0))
    s.blit(s2, (0, s1.get_height()))
    return s

def font_skin(scene, name) :
    """if no pics create from font"""
    surface = scene.font.render(name, False, scene.theme['txt_color'])
    return surface

def blit_clip(src, dest, margins=None) :
    """blit a portion of src"""
    surf = dest.copy()
    surf.blit(src, (0, 0), margins)
    return surf
