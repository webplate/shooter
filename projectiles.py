#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parameters import *

class Projectile() :
    """projectile positions should be accessed with position(index)"""
    def __init__(self, scene, surface) :
        self.scene = scene
        #load in scene
        self.scene.content.append(self)
        self.surface = surface
        self.positions = [] #floats for exact positions
        self.ally = False
        self.pulse = BASEPULSE
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

    def in_screen(self, pos) :
        #bad if outside screen
        if (pos[0] > self.scene.limits[0] or pos[1] > self.scene.limits[1]
        or pos[0] + self.width < 0 or pos[1] + self.height < 0) :
            return False
        else :
            return True

    def update(self) :
        #delete if outside screen
        self.positions = [pos for pos in self.positions if self.in_screen(pos)]

class Bullets(Projectile) :
    """a map of bullets
    """
    def __init__(self, scene, direction, surface) :
        Projectile.__init__(self, scene, surface)
        self.direction = direction

    def update(self, interval, time) :
        #should consider time passed
        offset = BULLET_SPEED * interval
        #move every projectile in one direction
        for index, projectile in enumerate(self.positions) :
            if self.direction == 'up' :
                self.positions[index] = (projectile[0],
                projectile[1]-offset, projectile[2])
            elif self.direction == 'down' :
                self.positions[index] = (projectile[0],
                projectile[1]+offset, projectile[2])
        Projectile.update(self)


class Blasts(Bullets) :
    """charged shots"""
    def __init__(self, scene, direction, surface) :
        Bullets.__init__(self, scene, direction, surface)

    def collided(self, index) :
        pass

    def damage(self, index) :
        #get power of charged shot
        amount = self.positions[index][2][1] * BLASTPOWER
        print amount
        return amount
