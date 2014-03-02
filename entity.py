#!/usr/bin/env python
# -*- coding: utf-8 -*-
import movement, tools

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
        #load image
        self.surface = self.scene.cont.surf(self.name)
        #layer for drawing on screen
        self.layer = 2
        #priority of update
        self.priority = 0

    def set_param(self, parameters) :
        self.parameters = parameters
        for p in self.parameters :
            setattr(self, p, self.parameters[p])

    def add(self) :
        """load in scene"""
        self.scene.content.append(self, self.priority)

    def remove(self) :
        """remove from scene"""
        self.scene.content.remove(self)

class Mobile(Actor) :
    """a mobile sprite
    """
    def __init__(self, scene, parameters={}) :
        Actor.__init__(self, scene, parameters)
        self._pos = (0, 0)
        if 'speed' not in parameters :
            self.speed = 0
        if 'trajectory' not in parameters :
            self.trajectory = None
        else :
            #a trajectory object to control position
            trajClass = getattr(movement, self.trajectory)
            self.movement = trajClass(self.scene, self)
        self.base_surface = self.surface
        self.center = tools.get_center(self.pos, self.surface)
        
    def _get_pos(self) :
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position
    def _set_pos(self, new_position) :
        self._pos = new_position[0], new_position[1]
    pos = property(_get_pos, _set_pos)
    
    def move(self, interval, time) :
        if self.trajectory != None :
            self._pos = self.movement.next_pos(self._pos, interval, time)
        
    def center_on(self, mobile) :
        x, y = mobile.pos
        w, h = mobile.surface.get_width()/2, mobile.surface.get_height()/2
        sw, sh = self.surface.get_width()/2, self.surface.get_height()/2
        self._pos = x + w - sw, y + h - sh 

    def update(self, interval, time) :
        self.center = tools.get_center(self.pos, self.surface)
        self.move(interval, time)


class Fragile(Mobile) :
    """this one can be hurt
    parameters should contain :
    -life
    """
    def __init__(self, scene, parameters) :
        Mobile.__init__(self, scene, parameters)
        self.killer = None
        self.last_hit = 0
        self.time_of_death = None
        #reward for killing
        self.reward = 1
        #fragile can explode
        self.end = Explosion(self.scene, self)
        #prepare score show if significant
        if self.reward > 99 :
            self.rew = Desc(self.scene, self)

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

    def die(self) :
        #remove of scene
        self.remove()
        #reward shooter
        self.killer.score += self.reward
        #explode
        self.end.add()
        if self.reward > 99 :
            #show reward
            self.rew.add()
        #play explosion sound at correct stereo position
        self.scene.cont.play('explosion', self.pos[0])
        
        
    def update(self, interval, time) :
        Mobile.update(self, interval, time)
        #change color for some time if hit recently
        if time < self.last_hit + self.scene.gameplay['flash_pulse'] :
            self.surface = self.scene.cont.hit[self.name]
        else :
            self.surface = self.scene.cont.surfaces[self.name]
        if self.life <= 0 :
            self.die()

class Fighter(Fragile) :
    """a shooting mobile sprite
    """
    def __init__(self, scene, parameters) :
        Fragile.__init__(self, scene, parameters)
        self.last_shoot = 0
        self.arms = {}
        #instantiate projectile maps for weapons
        if 'weapons' in parameters :
            for weapon in parameters['weapons'] :
                self.new_weapon(weapon)
        self.score = 0

    def add(self) :
        Fragile.add(self)
        for arm in self.arms :
            p_map = self.arms[arm]
            #add projectile map to scene container
            p_map.add()

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
            #limit fire rate
            if time > self.last_shoot + w.cooldown :
                x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
                w.positions.append((x, y, [self]))
                self.last_shoot = time

    def update(self, interval, time) :
        Fragile.update(self, interval, time)
        #autofire
        self.shoot(time, 'Bullet')
            

class ChargeFighter(Fighter) :
    """a charging mobile sprite
    charge_rate"""
    def __init__(self, scene, parameters) :
        Fighter.__init__(self, scene, parameters)
        self.charge = 0.
        #can have a charge display following fighter
        self.aura = Charge(self.scene, self)

    def add(self) :
        Fighter.add(self)
        self.aura.add()

    def shoot(self, time, weapon, power=None) :
        w = self.arms[weapon]
        #most projectiles aren't charged
        if weapon == 'Bullet' :
            #limit fire rate and stop when charging
            if (time > self.last_shoot + w.cooldown
            and self.charge == 0 ) :
                x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
                w.positions.append((x, y, [self]))
                self.scene.cont.play('shoot', self.pos[0])
                self.last_shoot = time
        #blast shot
        elif weapon == 'Blast' :
            x, y = (self.center[0]-w.width/2, self.center[1]-w.height/2)
            w.positions.append((x, y, [self, power]))
            

    def die(self) :
        Fighter.die(self)
        #remove also charge display
        self.aura.remove()

class Ship(ChargeFighter) :
    """A ship controlled by player and shooting
    """
    def __init__(self, scene, player, parameters) :
        ChargeFighter.__init__(self, scene, parameters)
        self.player = player
        #keep ref of maximum life
        self.max_life = self.life
        #a base name to derive alternate states
        self.base_name = self.name
        #preload oriented sprites
        self.scene.cont.surf('-' + self.base_name)
        self.scene.cont.surf(self.base_name + '-')
        
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
        new_center = tools.get_center(new_pos, self.surface)
        #do not step outside screen
        if (new_center[0] < self.scene.limits[0] and new_center[0] > 0
        and new_center[1] < self.scene.limits[1] and new_center[1] > 0) :
            self._pos = new_pos

    def die(self) :
        ChargeFighter.die(self)
        #player is dead
        self.player.alive = False

    def update(self, interval, time) :
        #show orientation of ship
        if not self.player.go_right and not self.player.go_left :
            self.name = self.base_name
        elif self.player.go_right :
            self.name = '-' + self.base_name
        elif self.player.go_left :
            self.name = self.base_name + '-'
            
        self.surface = self.scene.cont.surf(self.name)
        ChargeFighter.update(self, interval, time)

class Follower(Mobile) :
    """a sprite following another"""
    def __init__(self, scene, parent, offset) :
        Mobile.__init__(self, scene)
        self.parent = parent
        self.offset = offset
        self.center_on(self.parent)
        #should be updated after parents
        self.priority = 1

    def move(self, interval, time) :
        """move to be centered on parent"""
        self.center_on(self.parent)
        new_pos = self._pos[0]+self.offset[0], self._pos[1]+self.offset[1]
        self._pos = new_pos

class Charge(Follower) :
    """showing the charge of ship"""
    def __init__(self, scene, parent, offset=(0, 0)) :
        #offset to show over ship
        Follower.__init__(self, scene, parent, offset)
        self.levels = [self.scene.cont.surf(' '),
        self.scene.cont.surf('B'),
        self.scene.cont.surf('BB'),
        self.scene.cont.surf('BBB')]
        #draw over background but under ship
        self.layer = 1

    def update(self, interval, time) :
        if self.parent.charge >= 1 :
            self.surface = self.levels[3]
        elif self.parent.charge > 0.5 :
            self.surface = self.levels[2]
        elif self.parent.charge > 0 :
            self.surface = self.levels[1]
        elif self.parent.charge == 0 :
            self.surface = self.levels[0]
        #center on parent at the end of update
        Follower.update(self, interval, time)

class Explosion(Mobile) :
    """showing explosion of ship at last standing point"""
    def __init__(self, scene, parent) :
        Mobile.__init__(self, scene)
        self.parent = parent
        self.levels = [self.scene.cont.surf('OOOOOOO'),
        self.scene.cont.surf('OOOOO'),
        self.scene.cont.surf('OOO')]
        self.pulse = self.scene.theme['explosion_pulse']
        #explosions are in front
        self.layer = 3

    def update(self, interval, time) :
        if time > self.parent.time_of_death + self.pulse*3 :
            #disappear after dissipation
            self.remove()
        elif time > self.parent.time_of_death + self.pulse*2 :
            self.surface = self.levels[2]
        elif time > self.parent.time_of_death + self.pulse :
            self.surface = self.levels[1]
        elif time > self.parent.time_of_death :
            self.surface = self.levels[0]
        self.center_on(self.parent)

class Desc(Mobile) :
    """showing descriptor on item"""
    def __init__(self, scene, parent, text='100', duration=500) :
        Mobile.__init__(self, scene)
        self.parent = parent
        self.surface = self.scene.cont.surf(text)
        self.duration = duration
        self.layer = 4

    def update(self, interval, time) :
        if time > self.parent.time_of_death + self.duration :
            self.remove()
        self.center_on(self.parent)

class Widget(Mobile):
    def __init__(self, scene, path, parameters, offset=(0, 0)) :
        Mobile.__init__(self, scene)
        self.path = path
        self.parameters = parameters
        self.offset = offset
        self.value = self.new_value()
        self.surface = self.skin(self.value)
        self.shape = self.surface.get_width(), self.surface.get_height()
        self.pos = (0, 0)
        self.align()
        #support delayed updates
        if 'low_flip' in self.parameters :
            self.low = True
            self.last_flip = 0
        else :
            self.low = False
        #draw interface over rest of scene
        self.layer = 5

    def new_value(self) :
        """gets a value deep in scene"""
        return getattr_deep(self.scene, self.path)
        
    def align(self) :
        #recompute coordinates
        if 'center' in self.parameters :
            self.pos = (self.scene.limits[0]/2-self.shape[0]/2+self.offset[0],
            self.scene.limits[1]/2-self.shape[1]/2+self.offset[1])
        if 'left' in self.parameters :
            self.pos = (self.offset[0], self.pos[1]+self.offset[1])
        if 'right' in self.parameters :
            self.pos = (self.scene.limits[0]-self.shape[0]+self.offset[0],
            self.pos[1]+self.offset[1])
        if 'top' in self.parameters :
            self.pos = (self.pos[0]+self.offset[0], self.offset[1])
        if 'bottom' in self.parameters :
            self.pos = (self.pos[0]+self.offset[0],
            self.scene.limits[1]-self.shape[1]+self.offset[1])

    def skin(self, value) :
        surface = self.scene.sfont.render(str(int(value)), False,
        self.scene.theme['txt_color'])
        return surface
        
    def update(self, interval, time) :
        #recompute surface
        new_value = self.new_value()
        if not self.low :
            if self.value != new_value :
                self.value = new_value
                self.surface = self.skin(new_value)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()
        else :
            if time > self.last_flip + 500 and self.value != new_value :
                self.value = new_value
                self.last_flip = time
                self.surface = self.skin(new_value)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape :
                    self.shape = new_shape
                    self.align()

class Score(Widget) :
    """shows score of player (id given by path)"""
    def new_value(self) :
        player = self.scene.players[self.path]
        #complete with leading zeros
        score = int(player.score)
        return score

    def skin(self, value) :
        value = str(value).rjust(5, '0')
        surface = self.scene.sfont.render(value, False,
        self.scene.theme['txt_color'])
        return surface

class Life(Widget) :
    """shows life bar of player (id given by path)"""
    def new_value(self) :
        player = self.scene.players[self.path]
        return float(player.life) / player.max_life

    def skin(self, value) :
        #load back sprite of life bar
        back = self.scene.cont.surf('_____')
        front = self.scene.cont.surf('+++++')
        w = front.get_width()
        h = front.get_height()
        size = int(w * value)
        #blit only a portion of life bar
        surf = tools.blit_clip(front, back, (0, 0, size, h))
        return surf


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

    def add(self) :
        """add projectile map to scene if it is the only one with such
        parameters"""
        if self not in self.scene.content :
            Actor.add(self)

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
            
