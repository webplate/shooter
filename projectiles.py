#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from parameters import *

class Projectile() :
    """projectile positions should be accessed with position(index)"""
    def __init__(self, direction, font, limits) :
        self.direction = direction
        self.positions = [] #floats for exact positions
        self.ally = False
        self.font = font
        self.limits = limits

    def position(self, index) :
        """give rounded position of a projectile"""
        pos = self.positions[index]
        return int(pos[0]), int(pos[1])

class Bullets(Projectile) :
    """a map of bullets
    """
    def __init__(self, direction, font, limits) :
        Projectile.__init__(self, direction, font, limits)
        self.surface = font.render('H', False, txt_color)
        self.array = pygame.surfarray.array2d(self.surface).astype(bool)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def update(self, interval) :
        #should consider time passed
        offset = BULLET_SPEED * interval
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                x, y = (pos[0], pos[1]-offset)
                #remove if outside screen
                if (x > self.limits[0] or x + self.width < 0
                or y > self.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y)
        elif self.direction == 'down' :
            for i, pos in enumerate(self.positions) :
                x, y = (pos[0], pos[1]+offset)
                #remove if outside screen
                if (x > self.limits[0] or x + self.width < 0
                or y > self.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y)
        
class Blasts(Projectile) :
    """charged shots"""
    def __init__(self, direction, font, limits) :
        Projectile.__init__(self, direction, font, limits)
        self.surface = font.render('Oo..oO', False, txt_color)
        self.array = pygame.surfarray.array2d(self.surface).astype(bool)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        
    def update(self, interval) :
        #should consider time passed
        offset = BULLET_SPEED * interval
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                x, y, p = (pos[0], pos[1]-offset, pos[2])
                #remove if outside screen
                if (x > self.limits[0] or x + self.width < 0
                or y > self.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y, p)
        elif self.direction == 'down' :
            for i, pos in enumerate(self.positions) :
                x, y, p = (pos[0], pos[1]+offset, pos[2])
                #remove if outside screen
                if (x > self.limits[0] or x + self.width < 0
                or y > self.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y, p)
