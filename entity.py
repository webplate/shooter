#!/usr/bin/env python
# -*- coding: utf-8 -*-
import surftools

def getattr_deep(start, attr):
    """useful function for accessing attributes of attributes..."""
    obj = start
    for part in attr.split('.'):
        obj = getattr(obj, part)
    return obj

class Actor(object) :
    """a parametrable actor of scene
    """
    def __init__(self, scene, parameters={}) :
        self.scene = scene
        #set attributes from parameters
        self.set_param(parameters)
        #must have a name
        if 'name' not in parameters :
            self.name = ' '
        #default is not ally
        if 'ally' not in parameters :
            self.ally = False
        #load in scene
        self.scene.content.append(self)
        #load image
        self.surface = self.scene.cont.surf(self.name)
        #layer for drawing on screen
        self.layer = 0

    def set_param(self, parameters) :
        self.parameters = parameters
        for p in self.parameters :
            setattr(self, p, self.parameters[p])

    def remove(self) :
        """remove from scene"""
        self.scene.content.remove(self)

class Mobile(Actor) :
    """a mobile sprite
    """
    def __init__(self, scene, parameters={}) :
        Actor.__init__(self, scene, parameters)
        if 'speed' not in parameters :
            self.speed = 0
        self.array = self.scene.cont.array[self.name]
        self.base_surface = self.surface
        self._pos = (0, 0)
        self.trajectory = None

    def _get_pos(self) :
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position
    def _set_pos(self, new_position) :
        self._pos = new_position[0], new_position[1]
    pos = property(_get_pos, _set_pos)
    
    def move(self, interval) :
        pass
        
    def center_on(self, mobile) :
        x, y = mobile.pos
        w, h = mobile.surface.get_width()/2, mobile.surface.get_height()/2
        sw, sh = self.surface.get_width()/2, self.surface.get_height()/2
        self._pos = x + w - sw, y + h - sh 

    def update(self, interval, time) :
        self.center = surftools.get_center(self.pos, self.surface)
        self.move(interval)


class Fragile(Mobile) :
    """this one can be hurt
    parameters should contain :
    -life
    """
    def __init__(self, scene, parameters) :
        Mobile.__init__(self, scene, parameters)
        #load and avoid duplicate
        self.hit_surface = self.scene.cont.hit[self.name]
        self.killer = None
        self.last_hit = 0
        self.time_of_death = None
        #fragile can explode
        self.end = Explosion(self.scene, self)

    def collided(self, projectile, index, time) :
        #persistent projectiles have damage pulse
        if time - self.last_hit > self.scene.gameplay['hit_pulse'] :
            self.last_hit = time
            #take damage
            self.life -= projectile.get_damage(index)
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
        if time > self.last_hit + self.scene.gameplay['flash_pulse'] :
            self.surface = self.base_surface
        if self.life <= 0 :
            self.die()

class Fighter(Fragile) :
    """a shooting mobile sprite
    charge_rate"""
    def __init__(self, scene, parameters) :
        Fragile.__init__(self, scene, parameters)
        self.last_shoot = 0
        self.arms = {}
        #instantiate projectile maps for weapons
        if 'weapons' in parameters :
            for weapon in parameters['weapons'] :
                self.new_weapon(weapon)
        self.charge = 0.
        self.score = 0
        #can have a charge display following fighter
        self.aura = Charge(self.scene, self,
        (0, -self.scene.theme['txt_inter']))

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

    def new_weapon(self, parameters) :
        #load and avoid duplicate in scene
        projectile_map = self.scene.cont.proj(parameters)
        #set map allied status
        projectile_map.ally = self.ally
        #keep trace of weapon
        self.arms.update({projectile_map.type : projectile_map})

    def shoot(self, time, weapon, power=None) :
        w = self.arms[weapon]
        #most projectiles aren't charged
        if weapon == 'Bullet' :
            #limit fire rate and stop when charging
            if (time > self.last_shoot + w.cooldown
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
        self.shoot(time, 'Bullet')
            

class Ship(Fighter) :
    """A ship controlled by player and shooting
    ally"""
    def __init__(self, scene, parameters) :
        Fighter.__init__(self, scene, parameters)
        self.trajectory = 'manual'

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
    def __init__(self, scene, parent, offset) :
        Mobile.__init__(self, scene)
        self.parent = parent
        self.offset = offset
        self.center_on(self.parent)
        #should be updated after parents
        self.scene.content.prioritize(self, 1)

    def move(self, interval) :
        """move to be centered on parent"""
        self.center_on(self.parent)
        new_pos = self._pos[0]+self.offset[0], self._pos[1]+self.offset[1]
        self._pos = new_pos

class Charge(Follower) :
    """showing the charge of ship"""
    def __init__(self, scene, parent, offset) :
        #offset to show over ship
        Follower.__init__(self, scene, parent, offset)
        self.levels = [self.scene.cont.surf(' '),
        self.scene.cont.surf('#'),
        self.scene.cont.surf('##'),
        self.scene.cont.surf('###')]

    def update(self, interval, time) :
        Follower.update(self, interval, time)
        if self.parent.charge >= 1 :
            self.surface = self.levels[3]
        elif self.parent.charge > 0.5 :
            self.surface = self.levels[2]
        elif self.parent.charge > 0 :
            self.surface = self.levels[1]
        elif self.parent.charge == 0 :
            self.surface = self.levels[0]

class Explosion(Follower) :
    """showing explosion of ship at last standing point"""
    def __init__(self, scene, parent, offset=(0, 0)) :
        Follower.__init__(self, scene, parent, offset)
        self.levels = [self.scene.cont.surf('0000000'),
        self.scene.cont.surf('00000'),
        self.scene.cont.surf('000')]
        self.pulse = self.scene.theme['explosion_pulse']

    def update(self, interval, time) :
        if self.parent.life <= 0 :
            Follower.update(self, interval, time)
            if time > self.parent.time_of_death + self.pulse*3 :
                self.remove()
            elif time > self.parent.time_of_death + self.pulse*2 :
                self.surface = self.levels[2]
            elif time > self.parent.time_of_death + self.pulse :
                self.surface = self.levels[1]
            elif time > self.parent.time_of_death :
                self.surface = self.levels[0]


class Widget(Mobile):
    def __init__(self, scene, path, parameters) :
        Mobile.__init__(self, scene, {})
        self.path = path
        self.parameters = parameters
        self.value = getattr_deep(self.scene, path)
        self.surface = self.scene.font.render(self.skin(self.value),
        False, self.scene.theme['txt_color'])
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
                self.surface = self.scene.font.render(self.skin(new_value),
                False, self.scene.theme['txt_color'])
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()
        else :
            if time > self.last_flip + 500 and self.value != new_value :
                self.value = new_value
                self.last_flip = time
                self.surface = self.scene.font.render(self.skin(new_value),
                False, self.scene.theme['txt_color'])
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()

# PROJECTILE MAPS ###############
#################################
class Projectile(Actor) :
    """projectile positions should be accessed with position(index)
    damage
    """
    def __init__(self, scene, parameters) :
        Actor.__init__(self, scene, parameters)
        self.positions = [] #floats for exact positions
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.center_offset = self.width/2, self.height/2
        self.to_remove = []

    def collided(self, index) :
        #mark_bullet for removal (if not already)
        if index not in self.to_remove :
            self.to_remove.append(index)

    def get_damage(self, index) :
        return self.damage

    def draw_position(self, index) :
        """give rounded position of a projectile surface"""
        pos = self.positions[index]
        return int(pos[0]), int(pos[1])

    def position(self, index) :
        """the physical position of projectile"""
        pos = self.positions[index]
        return int(pos[0]+self.center_offset[0]), int(pos[1]+self.center_offset[1])

    def in_screen(self, pos) :
        #bad if outside screen
        if (pos[0] > self.scene.limits[0] or pos[1] > self.scene.limits[1]
        or pos[0] + self.width < 0 or pos[1] + self.height < 0) :
            return False
        else :
            return True

    def update(self) :
        remaining_positions = []
        for i in range(len(self.positions)) :
            #delete if marked
            if i not in self.to_remove :
                #delete if outside screen
                if self.in_screen(self.positions[i]) :
                    remaining_positions.append(self.positions[i])
        self.positions = remaining_positions
        self.to_remove = []

class Bullet(Projectile) :
    """a map of bullets
    direction
    speed
    """
    def __init__(self, scene, parameters) :
        Projectile.__init__(self, scene, parameters)

    def update(self, interval, time) :
        #should consider time passed
        offset = self.speed * interval
        #move every projectile in one direction
        for index, projectile in enumerate(self.positions) :
            if self.direction == 'up' :
                self.positions[index] = (projectile[0],
                projectile[1]-offset, projectile[2])
            elif self.direction == 'down' :
                self.positions[index] = (projectile[0],
                projectile[1]+offset, projectile[2])
        Projectile.update(self)


class Blast(Bullet) :
    """charged shots
    power
    """
    def __init__(self, scene, parameters) :
        Bullet.__init__(self, scene, parameters)

    def collided(self, index) :
        pass

    def get_damage(self, index) :
        #get power of charged shot
        amount = self.positions[index][2][1] * self.power
        return amount
            
