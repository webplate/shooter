#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
from parameters import *
import entity, projectiles


def load_content(scene) :
    #fighters
    ship = entity.Ship(scene, (0,scene.limits[1]-2*txt_inter), 'ship')
    fighter = entity.Fighter(scene, (scene.limits[0]/2,0), 'target')
    fighter2 = entity.Fighter(scene, (scene.limits[0]/3,200), 'target')
    #projectile maps
    ship_bullets = projectiles.Bullets(scene, 'up')
    ship_blasts = projectiles.Blasts(scene, 'up')
    targ_bullets = projectiles.Bullets(scene, 'down')
    #link fighters to projectile maps
    ship.new_weapon(ship_bullets)
    ship.new_weapon(ship_blasts)
    fighter.new_weapon(targ_bullets)
    fighter2.new_weapon(targ_bullets)
    content = [ship, fighter, fighter2, ship_bullets, ship_blasts,
    targ_bullets]
    return content

class Scene():
    def __init__(self, font) :
        self.font = font
        self.limits = window_size
        self.content = []
        self.content = load_content(self)
        for item in self.content :
            if isinstance(item, entity.Ship) :
                self.ship = item
                break
        self.lst_sprites = []
        self.update(0)

    def update(self, interval = 0) :
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
            elif isinstance(item, projectiles.Projectile) :
                for i in range(len(item.positions)) :
                    pos = item.position(i)
                    self.lst_sprites.append((pos, item.surface))
                    if item.ally :
                        self.ship_proj_map.append((pos, item.array))
                    else :
                        self.target_proj_map.append((pos, item.array))
