#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity


class Scene():
    def __init__(self, content) :
        self.content = content
        self.update(0)

    def list_sprites(self) :
        '''explore sprites in drawing order'''
        for item in self.content :
            yield item.pos, item.surface
            #draw projectile maps
            if isinstance(item, entity.Fighter) :
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
            #shoot and stuff
            item.update()
            #projectiles of object move according to time
            item.bullets.update(interval)
            #populate collision maps
            if isinstance(item, entity.Ship) :
                self.ship_map.append((item.pos, item.array))
                for i in range(len(item.bullets.positions)) :
                    pos = item.bullets.position(i)
                    self.ship_proj_map.append((pos, item.bullets.array))
            elif isinstance(item, entity.Fighter) :
                self.target_map.append((item.pos, item.array))
                for i in range(len(item.bullets.positions)) :
                    pos = item.bullets.position(i)
                    self.target_proj_map.append((pos, item.bullets.array))

