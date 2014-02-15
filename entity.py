#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import projectiles
from parameters import *

def get_center(pos, surface) :
    center = (pos[0]+surface.get_width()/2, pos[1]+surface.get_height()/2)
    return center

class Mobile_sprite() :
    '''a mobile sprite'''
    def __init__(self, pos, identity, font) :
        self.pos = pos
        self.identity = identity
        self.speed = 0
        self.orientation = 0
        self.surface = font.render(identity, False, txt_color)
        self.array = pygame.surfarray.array_alpha(self.surface)
        self.center = get_center(self.pos, self.surface)

    def update(self) :
        self.center = get_center(self.pos, self.surface)

class Fighter(Mobile_sprite) :
    '''a shooting mobile sprite'''
    def __init__(self, pos, identity, font, limits) :
        Mobile_sprite.__init__(self, pos, identity, font)
        bullet_sprite = font.render('d', False, txt_color)
        self.bullets = projectiles.Bullets('down', bullet_sprite, limits)
        self.fire_cooldown = BASE_COOLDOWN
        self.last_shoot = 0

    def shoot(self) :
        if pygame.time.get_ticks() > self.last_shoot + self.fire_cooldown :
            self.bullets.positions.append(self.center)
            self.last_shoot = pygame.time.get_ticks()

    def update(self) :
        Mobile_sprite.update(self)
        self.shoot()

class Ship(Fighter) :
    '''A ship controlled by player and shooting'''
    def __init__(self, pos, identity, font, limits) :
        Fighter.__init__(self, pos, identity, font, limits)
        bullet_sprite = font.render('p', False, txt_color)
        self.bullets = projectiles.Bullets('up', bullet_sprite, limits)
        self.speed_power = BASE_POWER
        self.limits = limits
        self.fire_cooldown = SHIP_COOLDOWN

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
        new_center = get_center(new_pos, self.surface)
        #do not step outside screen
        if (new_center[0] < self.limits[0] and new_center[0] > 0
        and new_center[1] < self.limits[1] and new_center[1] > 0) :
            self.pos = new_pos
