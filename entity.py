#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import projectiles
from parameters import *

class Mobile_sprite() :
    '''a mobile sprite'''
    def __init__(self, pos, identity, font) :
        self.pos = pos
        self.identity = identity
        self.speed = 0
        self.orientation = 0
        self.surface = font.render(identity, False, txt_color)
        self.center = (self.pos[0]+self.surface.get_width()/2,
        self.pos[1]+self.surface.get_height()/2)

    def update(self) :
        self.center = (self.pos[0]+self.surface.get_width()/2,
        self.pos[1]+self.surface.get_height()/2)


class Ship(Mobile_sprite) :
    '''A ship controlled by player and shooting'''
    def __init__(self, pos, identity, font, limits) :
        Mobile_sprite.__init__(self, pos, identity, font)
        self.speed_power = BASE_POWER
        bullet_sprite = font.render('p', False, txt_color)
        self.bullets = projectiles.Bullets('up', bullet_sprite, limits)
        self.limits = limits

    def move(self, direction, interval) :
        #should consider time passed
        offset = self.speed_power * interval
        if direction == 'right' :
            new_pos = self.pos[0]+offset, self.pos[1]
        elif direction == 'left' :
            new_pos = self.pos[0]-offset, self.pos[1]
        elif direction == 'up' :
            new_pos = self.pos[0], self.pos[1]-offset
        elif direction == 'down' :
            new_pos = self.pos[0], self.pos[1]+offset
        new_center = (new_pos[0]+self.surface.get_width()/2,
        new_pos[1]+self.surface.get_height()/2)
        #do not step outside screen
        if (new_center[0] < self.limits[0] and new_center[0] > 0
        and new_center[1] < self.limits[1] and new_center[1] > 0) :
            self.pos = new_pos
        self.update()

    def shoot(self) :
        self.bullets.positions.append(self.center)
