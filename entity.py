#!/usr/bin/env python
# -*- coding: utf-8 -*-
import surftools
from parameters import *

class Mobile_sprite() :
    """a mobile sprite"""
    def __init__(self, scene, pos, surface) :
        self.scene = scene
        #load in scene
        self.scene.content.append(self)
        self._pos = pos
        self.surface = surface
        self.speed = 0
        self.ally = False
        self.trajectory = None
        self.life = BASELIFE
        self.last_hit = 0
        self.array = surftools.make_array(self.surface)
        self.center = surftools.get_center(self.pos, self.surface)

    def _get_pos(self) :
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position
    pos = property(_get_pos)
    
    def move(self, interval) :
        pass
    
    def collided(self, projectile, index, time) :
        #persistent projectiles have damage pulse
        if time - self.last_hit > projectile.pulse :
            #take damage
            self.life -= projectile.damage(index)
            self.last_hit = time

    def die(self) :
        #remove of scene
        self.scene.content.remove(self)
        #reward shooter
        if not self.ally :
            self.scene.player.score += 1

    def update(self, interval) :
        self.center = surftools.get_center(self.pos, self.surface)
        self.move(interval)
        if self.life < 0 :
            self.die()

class Fighter(Mobile_sprite) :
    """a shooting mobile sprite"""
    def __init__(self, scene, pos, surface) :
        Mobile_sprite.__init__(self, scene, pos, surface)
        self.fire_cooldown = BASE_COOLDOWN
        self.last_shoot = 0
        self.weapons = {}
        self.charge = 0.
        self.aura = None
    
    def move(self, interval) :
        if self.trajectory == None :
            offset = interval * TARGET_SPEED
            #move only if far enough
            distance = abs(self.center[0] - self.scene.ship.center[0])
            if distance > offset  :
                if self.scene.ship.center[0] > self.center[0] :
                    self._pos = self._pos[0] + offset, self._pos[1]
                elif self.scene.ship.pos[0] < self.center[0] :
                    self._pos = self._pos[0] - offset, self._pos[1]

    def new_weapon(self, projectile_map) :
        #set map allied status
        projectile_map.ally = self.ally
        #keep trace of weapon
        self.weapons.update({str(projectile_map.__class__) : projectile_map})

    def shoot(self, time, weapon='projectiles.Bullets', power=None) :
        w = self.weapons[weapon]
        #most projectiles aren't charged
        if power == None :
            #limit fire rate and stop when charging
            if (time > self.last_shoot + self.fire_cooldown
            and self.charge == 0 ) :
                x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
                w.positions.append((x, y))
                self.last_shoot = time
        else :
            x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
            w.positions.append((x, y, power))

    def die(self) :
        Mobile_sprite.die(self)
        #remove of scene if necessary
        if self.aura != None :
            self.scene.content.remove(self.aura)
        
    def update(self, interval, time) :
        Mobile_sprite.update(self, interval)
        #autofire
        self.shoot(time)
        #create charging blast if necessary
        if self.charge > 0 and self.aura == None :
            self.aura = Charge(self.scene, self)

class Ship(Fighter) :
    """A ship controlled by player and shooting"""
    def __init__(self, scene, pos, surface) :
        Fighter.__init__(self, scene, pos, surface)
        self.trajectory = 'manual'
        self.ally = True
        self.speed = BASE_SPEED
        self.fire_cooldown = SHIP_COOLDOWN
        self.life = SHIPLIFE

    def fly(self, direction, interval) :
        #should consider time passed
        offset = self.speed * interval
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

    def die(self) :
        Fighter.die(self)
        #player is dead
        self.scene.player.alive = False
        print 'Score : ', self.scene.player.score


class Charge(Mobile_sprite) :
    """showing the charge of ship"""
    def __init__(self, scene, ship) :
        self.scene = scene
        self.ship = ship
        self.pos = self.ship.pos
        Mobile_sprite.__init__(self, scene, self.ship.pos,
        self.scene.font.render('', False, txt_color))
        self.levels = [self.scene.font.render('', False, txt_color),
        self.scene.font.render('#', False, txt_color),
        self.scene.font.render('##', False, txt_color),
        self.scene.font.render('###', False, txt_color)]

    def shift_pos(self) :
        self.pos = self.ship.pos[0], self.ship.pos[1]+txt_inter

    def update(self, interval, time) :
        if self.ship.charge >= 1 :
            self.surface = self.levels[3]
        elif self.ship.charge > 0.5 :
            self.surface = self.levels[2]
        elif self.ship.charge > 0 :
            self.surface = self.levels[1]
        elif self.ship.charge == 0 :
            self.surface = self.levels[0]
        self.shift_pos()
        Mobile_sprite.update(self, interval)
