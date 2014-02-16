#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity, projectiles


def load_content(font) :
    #fighters
    ship = entity.Ship((0,window_size[1]-2*txt_inter),
    'ship', font, window_size)
    fighter = entity.Fighter((window_size[0]/2,0),
    'target', font, window_size)
    fighter2 = entity.Fighter((window_size[0]/3,200),
    'target', font, window_size)
    #projectile maps
    ship_bullets = projectiles.Bullets('up', font, window_size)
    targ_bullets = projectiles.Bullets('down', font, window_size)
    #link fighters to projectile maps
    ship.new_weapon(ship_bullets)
    fighter.new_weapon(targ_bullets)
    fighter2.new_weapon(targ_bullets)
    content = [ship, fighter, fighter2, ship_bullets, targ_bullets]
    return content

class Scene():
    def __init__(self, font) :
        self.content = load_content(font)
        for item in self.content :
            if isinstance(item, entity.Ship) :
                self.ship = item
                break
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
