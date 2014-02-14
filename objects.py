#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
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


class Bullets() :
    '''a map of bullets'''
    def __init__(self, direction, sprite) :
        self.direction = direction
        self.positions = []
        self.sprite = sprite


    def update(self, interval) :
        if self.direction == 'up' :
            for i, pos in enumerate(self.positions) :
                #should consider time passed
                offset = BULLET_SPEED * interval
                self.positions[i] = (pos[0], pos[1]-offset)


class Ship(Mobile_sprite) :
    '''A ship controlled by player and shooting'''
    def __init__(self, pos, identity, font, limits) :
        Mobile_sprite.__init__(self, pos, identity, font)
        self.speed_power = BASE_POWER
        bullet_sprite = font.render('p', False, txt_color)
        self.bullets = Bullets('up', bullet_sprite)
        self.limits = limits

    def move(self, direction, interval) :
        #should consider time passed
        offset = self.speed_power * interval
        if direction == 'right' :
            self.pos = self.pos[0]+offset, self.pos[1]
        elif direction == 'left' :
            self.pos = self.pos[0]-offset, self.pos[1]
        elif direction == 'up' :
            self.pos = self.pos[0], self.pos[1]-offset
        elif direction == 'down' :
            self.pos = self.pos[0], self.pos[1]+offset
        #do not step outside screen
        if self.center[0] > self.limits[0] :
            self.pos = self.limits[0], self.center[1]
        elif self.center[0] < 0 :
            self.pos = 0, self.center[1]
        if self.pos[1] > self.limits[1] :
            self.pos = self.center[0], self.limits[1]
        elif self.center[1] < 0 :
            self.pos = self.center[0], 0

    def shoot(self) :
        self.bullets.positions.append(self.center)
