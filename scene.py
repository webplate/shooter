#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity

class Scene():
    def __init__(self, content):
        self.content = content
        self.update(0)

    def list_sprites(self) :
        for item in self.content :
            yield item.pos, item.surface
            #draw projectile maps
            if isinstance(item, entity.Ship) :
                projectiles = item.bullets
                for pos in projectiles.positions :
                    yield pos, projectiles.surface


    def update(self, interval) :
        #collision maps
        self.ship_map = []
        self.target_map = []
        self.ship_proj_map = []
        self.target_proj_map = []
        #explore scene
        for item in self.content :
            if isinstance(item, entity.Ship) :
                #shoot and stuff
                item.update()
                #projectiles of object
                projectiles = item.bullets
                #move according to time
                projectiles.update(interval)
                #populate collision map
                self.ship_map.append((item.pos, item.surface))
                for pos in projectiles.positions :
                    self.ship_proj_map.append((pos, projectiles.surface))
            elif isinstance(item, entity.Fighter) :
                item.update()
                projectiles = item.bullets
                projectiles.update(interval)
                self.target_map.append((item.pos, item.surface))
                for pos in projectiles.positions :
                    self.target_proj_map.append((pos, projectiles.surface))
