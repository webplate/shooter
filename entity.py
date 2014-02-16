#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import surftools
from parameters import *

class Mobile_sprite() :
    """a mobile sprite"""
    def __init__(self, scene, pos, identity) :
        self.scene = scene
        self._pos = pos
        self.identity = identity
        self.ally = False
        self.speed = 0
        self.orientation = 0
        if self.identity == 'ship' :
            self.surface = surftools.load_image('ship.png')
            self.array = pygame.surfarray.array_alpha(self.surface).astype(bool)
        else :
            self.surface = self.scene.font.render(identity, False, txt_color)
            self.array = pygame.surfarray.array2d(self.surface).astype(bool)
        
        self.center = surftools.get_center(self.pos, self.surface)

    def update(self, interval=0) :
        self.center = surftools.get_center(self.pos, self.surface)

    def _get_pos(self) :
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position
    pos = property(_get_pos)

class Fighter(Mobile_sprite) :
    """a shooting mobile sprite"""
    def __init__(self, scene, pos, identity) :
        Mobile_sprite.__init__(self, scene, pos, identity)
        self.fire_cooldown = BASE_COOLDOWN
        self.last_shoot = 0
        self.weapons = {}
        self.charge = 0
        self.aura = None
        #add new object in scene
        self.scene.content.append(self.aura)

    def new_weapon(self, projectile_map) :
        #set map allied status
        projectile_map.ally = self.ally
        #keep trace of weapon
        self.weapons.update({str(projectile_map.__class__) : projectile_map})

    def shoot(self, weapon='projectiles.Bullets', power=None) :
        w = self.weapons[weapon]
        #most projectiles aren't charged
        if power == None :
            #limit fire rate and stop when charging
            if (pygame.time.get_ticks() > self.last_shoot + self.fire_cooldown
            and self.charge == 0 ) :
                x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
                w.positions.append((x, y))
                self.last_shoot = pygame.time.get_ticks()
        else :
            x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
            w.positions.append((x, y, power))
    
    def update(self, interval=0) :
        Mobile_sprite.update(self)
        self.shoot()
        if self.charge > 0 :
            if self.aura == None :
                self.aura = Charge(self.scene, self, '')
            self.aura.update(self.charge)

class Ship(Fighter) :
    """A ship controlled by player and shooting"""
    def __init__(self, scene, pos, identity) :
        Fighter.__init__(self, scene, pos, identity)
        self.ally = True
        self.speed_power = BASE_POWER
        self.fire_cooldown = SHIP_COOLDOWN

    def move(self, direction, interval) :
        #should consider time passed
        offset = self.speed_power * interval
        if direction == 'right' :
            new_pos = self._pos[0]+offset, self._pos[1]
        elif direction == 'left' :
            new_pos = self._pos[0]-offset, self._pos[1]
        elif direction == 'up' :
            new_pos = self._pos[0], self._pos[1]-offset
        elif direction == 'down' :
            new_pos = self._pos[0], self._pos[1]+offset
        new_center = surftools.get_center(new_pos, self.surface)
        #do not step outside screen
        if (new_center[0] < self.scene.limits[0] and new_center[0] > 0
        and new_center[1] < self.scene.limits[1] and new_center[1] > 0) :
            self._pos = new_pos

class Charge(Mobile_sprite) :
    """showing the charge of ship"""
    def __init__(self, scene, ship, identity) :
        self.ship = ship
        self.pos = self.ship.pos
        Mobile_sprite.__init__(self, scene, self.pos, identity)
        self.levels = [self.scene.font.render('.....', False, txt_color),
        self.scene.font.render('_____', False, txt_color),
        self.scene.font.render('ooooo', False, txt_color),
        self.scene.font.render('OOOOO', False, txt_color)]
        self.arrays = [ pygame.surfarray.array2d(surface).astype(bool)
        for surface in self.levels ]
        
    def update(self, charge) :
        self.pos = self.ship.pos
        if charge == 0 :
            self.surface = self.levels[0]
            self.array = self.arrays[0]
        Mobile_sprite.update(self)
