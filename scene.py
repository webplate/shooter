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

    def collision_maps(self) :
        #special objects instead of dicts ???
        self.ship_map = {}
        self.target_map = {}
        self.proj_map = {}
        for item in self.content :
            if isinstance(item, entity.Ship) :
                if item.array in self.ship_map :
                    ship_map[item.array].append(item.pos)
                else :
                    self.ship_map.update({item.array : [item.pos]})
                projectiles = item.bullets
                for pos in projectiles.positions :
                    if projectiles.array in self.proj_map :
                        proj_map[projectiles.array].append(pos)
                    else :
                        self.ship_map.update({projectiles.array : [pos]})
            else :
                if item.array in self.target_map :
                    target_map[item.array].append(item.pos)
                else :
                    self.target_map.update({item.array : [item.pos]})
                
    def update(self) :
        self.collision_maps()
