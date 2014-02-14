#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from parameters import *

class Mobile_sprite():
    '''a mobile sprite'''
    def __init__(self, pos, identity, font):
        self.pos = pos
        self.identity = identity
        self.speed = 0
        self.orientation = 0
        self.surface = font.render(identity, False, txt_color)


class Ship(Mobile_sprite) :
    def __init__(self, pos, identity, font) :
        Mobile_sprite.__init__(self, pos, identity, font)
        self.speed_power = 1
    def move(self, direction, interval) :
        #should consider time passed
        offset = self.speed_power * interval
        if direction == 'right' :
            self.pos = self.pos[0]+offset, self.pos[1]
        elif direction == 'left' :
            self.pos = self.pos[0]-offset, self.pos[1]
        
