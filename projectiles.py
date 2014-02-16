#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from parameters import *

class Positions() :
    '''store exact position as float, give rounded position'''
    def __init__(self, pos) :
        self.position = pos
        self._pos = int(pos[0]), int(pos[1])

class Bullets() :
    '''a map of bullets'''
    def __init__(self, direction, surface, limits) :
        self.direction = direction
        self.positions = [] #float for exact positions
        self.surface = surface
        self.array = pygame.surfarray.array_alpha(self.surface)
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.limits = limits

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

    
    def position(self, index) :
        '''give rounded position of a projectile'''
        pos = self.positions[index]
        return int(pos[0]), int(pos[1])
        
