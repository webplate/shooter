#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from parameters import *
import entity, projectiles

class Scene():
    def __init__(self, font) :
        self.font = font
        self.limits = window_size
        self.content = []
        self.load_content()
        for item in self.content :
            if isinstance(item, entity.Ship) :
                self.ship = item
                break
        self.lst_sprites = []
        self.update()

    def load_fighter(self, identity) :
        coord = random.randint(0, self.limits[0]), 0
        fighter = entity.Fighter(self, coord, identity)
        #projectile maps
        targ_bullets = projectiles.Bullets(self, 'down')
        #link fighters to projectile maps
        fighter.new_weapon(targ_bullets)

    def load_ship(self, identity) :
        ship = entity.Ship(self, (0,self.limits[1]-2*txt_inter), identity)
        ship_bullets = projectiles.Bullets(self, 'up')
        ship_blasts = projectiles.Blasts(self, 'up')
        ship.new_weapon(ship_bullets)
        ship.new_weapon(ship_blasts)
        
    def load_content(self) :
        self.load_ship('ship')


    def collide(self, proj_map, target_map) :
        for xP, yP, itemP, index in proj_map :
            for xT, yT, xTe, yTe, itemT in target_map :
                if (xP < xTe and xP > xT
                and yP < yTe and yP > yT) :
                    #in range for per pixel collision detection
                    if itemT.array[xP - xT, yP - yT] :
                        #remove or not colliding projectile
                        #hurt or not entity
                        itemP.collided(index)
                        itemT.collided(itemP, index)
                        
        
    def update(self, interval = 0) :
        #collision maps
        ship_map = []
        target_map = []
        ship_proj_map = []
        target_proj_map = []
        #sprite list for drawing
        self.lst_sprites = []
        self.nb_fighters = 0
        #explore scene
        for item in self.content :
            #shoot and stuff
            item.update(interval)
            if isinstance(item, entity.Mobile_sprite) :
                x, y = item.pos
                #prepare sprite list for drawing
                self.lst_sprites.append(((x, y), item.surface))
                #populate collision maps
                width, height = item.array.shape
                identifier = (x, y, x+width, y+height, item)
                if item.ally :
                    ship_map.append(identifier)
                else :
                    self.nb_fighters += 1
                    target_map.append(identifier)
            elif isinstance(item, projectiles.Projectile) :
                for i in range(len(item.positions)) :
                    x, y = item.position(i)
                    self.lst_sprites.append(((x, y), item.surface))
                    if item.ally :
                        ship_proj_map.append((x, y, item, i))
                    else :
                        target_proj_map.append((x, y, item, i))
        #detect collisions and update accordingly
        self.collide(ship_proj_map, target_map)
        self.collide(target_proj_map, ship_map)
        #evolution of scenery
        if self.nb_fighters < 3 :
            self.load_fighter('target')
    
