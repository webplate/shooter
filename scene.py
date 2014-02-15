#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity

def is_round(pos) :
    return isinstance(pos[0], int) and isinstance(pos[1], int)
        
class Scene():
    def __init__(self, content):
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
            #populate collision map
            if isinstance(item, entity.Ship) :
                if not is_round(item.pos) : print 'not round'
                self.ship_map.append((item.pos, item.array))
                for pos in item.bullets.positions :
                    if not is_round(pos) : print 'not round'
                    self.ship_proj_map.append((pos, item.bullets.array))
            elif isinstance(item, entity.Fighter) :
                if not is_round(item.pos) : print 'not round'
                self.target_map.append((item.pos, item.array))
                for pos in item.bullets.positions :
                    if not is_round(pos) : print 'not round'
                    self.target_proj_map.append((pos, item.bullets.array))
