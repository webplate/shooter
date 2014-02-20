#!/usr/bin/env python
# -*- coding: utf-8 -*-
import surftools
from parameters import *

def getattr_deep(start, attr):
    """useful function for accessing attributes of attributes..."""
    obj = start
    for part in attr.split('.'):
        obj = getattr(obj, part)
    return obj

class Mobile() :
    """a mobile sprite"""
    def __init__(self, scene, pos, name) :
        self.scene = scene
        #load in scene
        self.scene.content.append(self)
        self.surface = self.scene.cont.surf(name)
        self.array = self.scene.cont.array[name]
        self.base_surface = self.surface
        self._pos = pos
        self.speed = 0
        self.trajectory = None
        self.ally = False

    def _get_pos(self) :
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position
    pos = property(_get_pos)

    def move(self, interval) :
        pass
        
    def center_on(self, mobile) :
        x, y = mobile.pos
        w, h = mobile.surface.get_width()/2, mobile.surface.get_height()/2
        sw, sh = self.surface.get_width()/2, self.surface.get_height()/2
        self._pos = x + w - sw, y + h - sh 
        
    def remove(self) :
        """remove from scene"""
        self.scene.content.remove(self)

    def update(self, interval, time) :
        self.center = surftools.get_center(self.pos, self.surface)
        self.move(interval)

class Fragile(Mobile) :
    """this one can be hurt"""
    def __init__(self, scene, pos, name) :
        Mobile.__init__(self, scene, pos, name)
        self.scene = scene
        self.hit_surface = self.scene.cont.hit[name]
        self.killer = None
        self.life = BASELIFE
        self.last_hit = 0
        self.time_of_death = None
        #fragile can explode
        self.end = Explosion(self.scene, self)
        
    def collided(self, projectile, index, time) :
        #persistent projectiles have damage pulse
        if time - self.last_hit > projectile.pulse :
            self.last_hit = time
            #take damage
            self.life -= projectile.damage(index)
            if self.life <= 0 :
                self.time_of_death = time
                #recognize killer in the distance
                proj = projectile.positions[index]
                self.killer = proj[2][0]
            #change color for some time
            self.surface = self.hit_surface

    def die(self) :
        #remove of scene
        self.remove()
        #reward shooter
        self.killer.score += 1
        
    def update(self, interval, time) :
        Mobile.update(self, interval, time)
        #return to unhit appearance
        if time > self.last_hit + HITPULSE :
            self.surface = self.base_surface
        if self.life <= 0 :
            self.die()

class Fighter(Fragile) :
    """a shooting mobile sprite"""
    def __init__(self, scene, pos, name) :
        Fragile.__init__(self, scene, pos, name)
        self.fire_cooldown = BASE_COOLDOWN
        self.last_shoot = 0
        self.weapons = {}
        self.charge = 0.
        self.aura = None
        self.speed = TARGET_SPEED
        self.score = 0
        #can have a charge display
        self.aura = Charge(self.scene, self)

    def move(self, interval) :
        if self.trajectory == None :
            offset =  self.speed * interval
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
        if weapon == 'projectiles.Bullets' :
            #limit fire rate and stop when charging
            if (time > self.last_shoot + self.fire_cooldown
            and self.charge == 0 ) :
                x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
                w.positions.append((x, y, [self]))
                self.last_shoot = time
        #blast shot
        else :
            x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
            w.positions.append((x, y, [self, power]))

    def die(self) :
        Fragile.die(self)
        #remove also charge display
        self.aura.remove()

    def update(self, interval, time) :
        Fragile.update(self, interval, time)
        #autofire
        self.shoot(time)
            

class Ship(Fighter) :
    """A ship controlled by player and shooting"""
    def __init__(self, scene, pos, name) :
        Fighter.__init__(self, scene, pos, name)
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

class Follower(Mobile) :
    """a sprite following another"""
    def __init__(self, scene, parent) :
        Mobile.__init__(self, self.scene, (0, 0), ' ')
        self.scene = scene
        self.parent = parent
        self.center_on(self.parent)

    def move(self, interval) :
        """move to be centered on parent"""
        self.center_on(self.parent)


class Charge(Follower) :
    """showing the charge of ship"""
    def __init__(self, scene, ship) :
        self.scene = scene
        self.ship = ship
        Follower.__init__(self, scene, self.ship)
        self.levels = [self.scene.cont.surf(' '),
        self.scene.cont.surf('#'),
        self.scene.cont.surf('##'),
        self.scene.cont.surf('###')]

    def update(self, interval, time) :
        Follower.update(self, interval, time)
        if self.ship.charge >= 1 :
            self.surface = self.levels[3]
        elif self.ship.charge > 0.5 :
            self.surface = self.levels[2]
        elif self.ship.charge > 0 :
            self.surface = self.levels[1]
        elif self.ship.charge == 0 :
            self.surface = self.levels[0]

class Explosion(Follower) :
    """showing explosion of ship at last standing point"""
    def __init__(self, scene, fragile) :
        self.scene = scene
        self.fragile = fragile
        Follower.__init__(self, scene, self.fragile)
        self.levels = [self.scene.cont.surf('0000000'),
        self.scene.cont.surf('00000'),
        self.scene.cont.surf('000')]
        self.pulse = EXPLOSIONPULSE

    def update(self, interval, time) :
        if self.fragile.life <= 0 :
            Follower.update(self, interval, time)
            if time > self.fragile.time_of_death + self.pulse*3 :
                self.remove()
            elif time > self.fragile.time_of_death + self.pulse*2 :
                self.surface = self.levels[2]
            elif time > self.fragile.time_of_death + self.pulse :
                self.surface = self.levels[1]
            elif time > self.fragile.time_of_death :
                self.surface = self.levels[0]


class Widget():
    def __init__(self, scene, path, parameters) :
        self.scene = scene
        #load in scene
        self.scene.content.append(self)
        self.path = path
        self.parameters = parameters
        self.value = getattr_deep(self.scene, path)
        self.surface = self.scene.font.render(self.skin(self.value), False, txt_color)
        self.shape = self.surface.get_width(), self.surface.get_height()
        self.pos = (0, 0)
        self.align()
        #support delayed updates
        if 'low_flip' in self.parameters :
            self.low = True
            self.last_flip = 0
        else :
            self.low = False

    def align(self) :
        #recompute coordinates
        if 'center' in self.parameters :
            self.pos = (self.scene.limits[0]/2-self.shape[0]/2,
            self.scene.limits[1]/2-self.shape[1]/2)
        if 'left' in self.parameters :
            self.pos = (0, self.pos[1])
        if 'right' in self.parameters :
            self.pos = (self.scene.limits[0]-self.shape[0], self.pos[1])
        if 'top' in self.parameters :
            self.pos = (self.pos[0], 0)
        if 'bottom' in self.parameters :
            
            self.pos = (self.pos[0], self.scene.limits[1]-self.shape[1])

    def skin(self, value) :
        return str(int(value))
        

    def update(self, interval, time) :
        #recompute surface
        new_value = getattr_deep(self.scene, self.path)  
        if not self.low :
            if self.value != new_value :
                self.value = new_value
                self.surface = self.scene.font.render(self.skin(new_value), False, txt_color)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()
        else :
            if time > self.last_flip + 500 and self.value != new_value :
                self.value = new_value
                self.last_flip = time
                self.surface = self.scene.font.render(self.skin(new_value), False, txt_color)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()
            
            
