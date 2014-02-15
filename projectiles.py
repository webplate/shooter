#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parameters import *

class Bullets() :
    '''a map of bullets'''
    def __init__(self, direction, sprite, limits) :
        self.direction = direction
        self.positions = []
        self.sprite = sprite
        self.width = sprite.get_width()
        self.height = sprite.get_height()
        self.limits = limits

    def update(self, interval) :
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                #should consider time passed
                offset = BULLET_SPEED * interval
                x, y = (pos[0], pos[1]-offset)
                #remove if outside screen
                if (x > self.limits[0] or x + self.width < 0
                or y > self.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y)
