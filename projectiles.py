#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parameters import *

class Projectile() :
    """projectile positions should be accessed with position(index)
    name
    damage
    """
    def __init__(self, scene, parameters) :
        self.scene = scene
        #set attributes from parameters
        self.set_param(parameters)
        #load in scene
        self.scene.content.append(self)
        self.surface = self.scene.cont.surf(self.name)
        self.positions = [] #floats for exact positions
        self.ally = False
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.center_offset = self.width/2, self.height/2
        self.to_remove = []

    def set_param(self, parameters) :
        self.parameters = parameters
        for p in self.parameters :
            setattr(self, p, self.parameters[p])

    def collided(self, index) :
        #mark_bullet for removal (if not already)
        if index not in self.to_remove :
            self.to_remove.append(index)

    def get_damage(self, index) :
        return self.damage

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
        remaining_positions = []
        for i in range(len(self.positions)) :
            #delete if marked
            if i not in self.to_remove :
                #delete if outside screen
                if self.in_screen(self.positions[i]) :
                    remaining_positions.append(self.positions[i])
        self.positions = remaining_positions
        self.to_remove = []

class Bullet(Projectile) :
    """a map of bullets
    direction
    speed
    """
    def __init__(self, scene, parameters) :
        Projectile.__init__(self, scene, parameters)

    def update(self, interval, time) :
        #should consider time passed
        offset = self.speed * interval
        #move every projectile in one direction
        for index, projectile in enumerate(self.positions) :
            if self.direction == 'up' :
                self.positions[index] = (projectile[0],
                projectile[1]-offset, projectile[2])
            elif self.direction == 'down' :
                self.positions[index] = (projectile[0],
                projectile[1]+offset, projectile[2])
        Projectile.update(self)


class Blast(Bullet) :
    """charged shots
    power
    """
    def __init__(self, scene, parameters) :
        Bullet.__init__(self, scene, parameters)

    def collided(self, index) :
        pass

    def get_damage(self, index) :
        #get power of charged shot
        amount = self.positions[index][2][1] * self.power
        return amount
