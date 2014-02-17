#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from parameters import *

class Projectile() :
    """projectile positions should be accessed with position(index)"""
    def __init__(self, scene, direction, identity) :
        self.scene = scene
        #load in scene
        self.scene.content.append(self)
        self.direction = direction
        self.identity = identity
        self.positions = [] #floats for exact positions
        self.ally = False
        self.surface = self.scene.font.render(self.identity, False, txt_color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.center_offset = self.width/2, self.height/2

    def collided(self, index) :
        l = len(self.positions)
        if l > 0 and index < l :
            self.positions.pop(index)

    def damage(self, index) :
        return BASEDAMAGE

    def draw_position(self, index) :
        """give rounded position of a projectile surface"""
        pos = self.positions[index]
        return int(pos[0]), int(pos[1])

    def position(self, index) :
        """the physical position of projectile"""
        pos = self.positions[index]
        return int(pos[0]+self.center_offset[0]), int(pos[1]+self.center_offset[1])


class Bullets(Projectile) :
    """a map of bullets
    """
    def __init__(self, scene, direction, identity) :
        Projectile.__init__(self, scene, direction, identity)


    def update(self, interval) :
        #should consider time passed
        offset = BULLET_SPEED * interval
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                x, y = (pos[0], pos[1]-offset)
                #remove if outside screen
                if (x > self.scene.limits[0] or x + self.width < 0
                or y > self.scene.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y)
        elif self.direction == 'down' :
            for i, pos in enumerate(self.positions) :
                x, y = (pos[0], pos[1]+offset)
                #remove if outside screen
                if (x > self.scene.limits[0] or x + self.width < 0
                or y > self.scene.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y)
        
class Blasts(Projectile) :
    """charged shots"""
    def __init__(self, scene, direction, identity) :
        Projectile.__init__(self, scene, direction, identity)

    def collided(self, index) :
        pass

    def damage(self, index) :
        amount = self.positions[index][2] * 5 + 1
        return amount
    
    def update(self, interval) :
        #should consider time passed
        offset = BULLET_SPEED * interval
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                x, y, p = (pos[0], pos[1]-offset, pos[2])
                #remove if outside screen
                if (x > self.scene.limits[0] or x + self.width < 0
                or y > self.scene.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y, p)
        elif self.direction == 'down' :
            for i, pos in enumerate(self.positions) :
                x, y, p = (pos[0], pos[1]+offset, pos[2])
                #remove if outside screen
                if (x > self.scene.limits[0] or x + self.width < 0
                or y > self.scene.limits[1] or y + self.height < 0) :
                    self.positions.remove(pos)
                else :
                    self.positions[i] = (x, y, p)
