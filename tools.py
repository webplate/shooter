#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, pygame
import parameters


def get_center(pos, w, h):
    center = (pos[0]+w/2., pos[1]+h/2.)
    return center


def get_pos_from_center(center, w, h):
    pos = (center[0]-w/2., center[1]-h/2.)
    return pos


def resource_path(relative):
    """path translator for pyinstaller
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def get_path(a1, a2, a3):
    return resource_path(os.path.join(a1, a2, a3))


def load_font(filename, size):
    myfontfile = resource_path(os.path.join('fonts', filename))
    return pygame.font.Font(myfontfile, size)


def load_sound(filename, scene):
    """load sound or not"""
    if scene.snd_pack['name'] is not None:
        path = get_path('sounds', scene.snd_pack['name'], filename + '.ogg')
        try:
            sound = pygame.mixer.Sound(path)
        except pygame.error:
            sound = None
    else:
        sound = None
    return sound


def load_stream(filename, scene):
    """load music track or not"""
    if scene.snd_pack['name'] is not None:
        path = get_path('sounds', scene.snd_pack['name'], filename + '.ogg')
        try:
            sound = pygame.mixer.music.load(path)
        except pygame.error:
            return False
        return True


def uniformize_surf(surface):
    """try to convert surface if necessary
    so that all our surf are of same type:
    no per pixel transparency"""
    

def load_image(name, theme, scene, alpha=True):
    """loads an image, prepares it for play
    or create a label if image absent
    or create a symmetry version if Vsym, Hsym or HVsym in name"""
    split = name.split(':')
    filename = split[0]
    keywords = split[1:]
    CWrot = False
    Hsym = False
    Vsym = False
    if 'Vsym' in keywords:
        Vsym = True
    if 'Hsym' in keywords:
        Hsym = True
    if 'CWrot' in keywords:
        CWrot = True
        
    if theme is not None:
        path = get_path('imgs', theme, filename + '.png')
        try:
            surface = pygame.image.load(path)
        except pygame.error:
            # if no corresponding png generate from label
            surface = font_skin(scene, filename)
        else:
            # strip of alpha channel for colorkey transparency and notmuch colors
            surface = surface.convert(parameters.COLORDEPTH)
            if alpha:
                # first pixel sets transparent color
                color = surface.get_at((0, 0))
                surface.set_colorkey(color)
            if Vsym or Hsym:
                #create a vertical sym of surface
                surface = pygame.transform.flip(surface, Vsym, Hsym)
            if CWrot:
                #create clockwise rotation of surface
                surface = pygame.transform.rotate(surface, -90)
    else:
        # no themepack: use labels as sprites
        surface = font_skin(scene, filename)
    return surface


def make_rect(w, h, color):
    surface = pygame.Surface((w, h))
    surface.fill(color)
    return surface


def make_array(surface):
    array = pygame.surfarray.array2d(surface)
    colorkey = surface.map_rgb(surface.get_colorkey())
    w, h = array.shape
    for i in range(w):
        for j in range(h):
            if array[i, j] != colorkey:
                array[i, j] = True
            else:
                array[i, j] = False
    return array


def make_white(surface):
    white = (255, 255, 255)
    black = (0, 0, 0)
    covered = make_array(surface)
    surface = pygame.Surface(surface.get_size(), depth = 8)
    surface.set_palette([black, white])
    w, h = covered.shape
    for i in range(w):
        for j in range(h):
            if covered[i,j]:
                surface.set_at((i, j), white)
            else:
                surface.set_at((i, j), black)
    surface.set_colorkey(black)
    return surface


def make_shadow(surface, scale=0.5):
    white = (255, 255, 255)
    black = (0, 0, 0)
    covered = make_array(surface)
    surface = pygame.Surface(surface.get_size(), depth = 8)
    surface.set_palette([black, white])
    w, h = covered.shape
    for i in range(w):
        for j in range(h):
            if covered[i, j]:
                surface.set_at((i, j), black)
            else:
                surface.set_at((i, j), white)
    # rescale shadow
    w, h = int(w*scale), int(h*scale)
    surface = pygame.transform.scale(surface, (w, h))
    surface.set_colorkey(white)
    return surface


def compose_surfaces(w, h, s1, s2, back=None):
    """gets two surfaces and blit them on a new one
    of size w,h
    """
    s = pygame.Surface((w, h))
    if back is not None:
        s.blit(back, (0, 0))
    s.blit(s1, (0, 0))
    s.blit(s2, (0, s1.get_height()))
    return s


def font_skin(scene, name):
    """if no pics create from font"""
    surface = scene.font.render(name, False, scene.theme['txt_color'])
    return surface


def blit_clip(src, dest, margins=None):
    """blit a portion of src"""
    surf = dest.copy()
    surf.blit(src, (0, 0), margins)
    return surf
