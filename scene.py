#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity

class Scene():
    def __init__(self, content):
        self.content = content
        self.update()

    def list_sprites(self) :
        for item in self.content :
            yield item.pos, item.surface
            #draw projectile maps
            if isinstance(item, entity.Ship) :
                projectiles = item.bullets
                for pos in projectiles.positions :
                    yield pos, projectiles.surface

    def list_entity(self) :
        for item in self.content :
            yield item.pos, item.array

    def list_projectile(self) :
        for item in self.content :
            if isinstance(item, entity.Ship) :
                projectiles = item.bullets
                for pos in projectiles.positions :
                    yield pos, projectiles.array

    def update(self) :
        self.ship_map = []
        self.target_map = []
        self.proj_map = []
        for item in self.content :
            if isinstance(item, entity.Mobile_sprite) :
                if isinstance(item, entity.Ship) :
                    self.ship_map.append((item.pos, item.array))
                    projectiles = item.bullets
                    for pos in projectiles.positions :
                        self.proj_map.append((pos, projectiles.array))
                else :
                    self.target_map.append((item.pos, item.array))
    
