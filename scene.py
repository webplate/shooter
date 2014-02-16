#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity, projectiles


class Scene():
    def __init__(self, content) :
        self.content = content
        self.lst_sprites = []
        self.update(0)

    def update(self, interval) :
        #collision maps
        self.ship_map = []
        self.target_map = []
        self.ship_proj_map = []
        self.target_proj_map = []
        self.lst_sprites = []
        #explore scene
        for item in self.content :
            #shoot and stuff
            item.update(interval)
            if isinstance(item, entity.Fighter) :
                #prepare sprite list for drawing
                self.lst_sprites.append((item.pos, item.surface))
                if item.ally :
                    #populate collision maps
                    self.ship_map.append((item.pos, item.array))
                else :
                    self.target_map.append((item.pos, item.array))
            elif isinstance(item, projectiles.Bullets) :
                for pos in item.positions :
                    self.lst_sprites.append((pos, item.surface))
                    if item.ally :
                        self.ship_proj_map.append((pos, item.array))
                    else :
                        self.target_proj_map.append((pos, item.array))
