# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random, math
import movement, tools, parameters


def getattr_deep(start, attr):
    """useful function for accessing attributes of attributes..."""
    obj = start
    for part in attr.split('.'):
        obj = getattr(obj, part)
    return obj


class Actor(object):
    """a parametrable actor of scene
    """
    def __init__(self, scene, params={}):
        self.scene = scene
        # set attributes from params
        self.set_param(params)
        # must have a name
        if not hasattr(self, 'name'):
            self.name = ' '
        # default is not ally
        if not hasattr(self, 'ally'):
            self.ally = False
        # layer for drawing on screen
        if not hasattr(self, 'layer'):
            self.layer = parameters.ACTORLAY
        # variables to intermitently check for target
        self.last_check = 0
        self.target = None
        # priority of update
        self.priority = parameters.BASEPRIOR

    def set_param(self, params):
        self.params = params
        for p in self.params:
            setattr(self, p, self.params[p])

    def add(self):
        """load in scene"""
        self.scene.content.append(self, self.priority)
        self.init_time = self.scene.now

    def remove(self):
        """remove from scene"""
        self.scene.content.remove(self)
    
    def search_enemy(self, time=None):
        target = None
        if time is None:
            time = self.scene.now
        # update targets every seconds
        if time > self.last_check + 1000:
            self.last_check = time
            # target healthier player !
            max_life = 0
            for item in self.scene.content:
                #~ print self.ally , item.ally
                is_enemy = self.ally != item.ally
                if is_enemy and hasattr(item, 'life'):
                    if item.life > max_life:
                        max_life = item.life
                        target = item
        return target
    
    def aim_angle(self):
        if self.target is not None:
            x, y = self.parent.center
            xT, yT = self.target.center
            #compute angle to target
            a = math.degrees(math.atan2((yT - y), (xT - x)))
            # angle relative to vertical axis
            a += 90
        else:
            a = 0
        return a
    


class Weapon(Actor):
    """generic weapon"""
    def __init__(self, scene, parent, params):
        Actor.__init__(self, scene, params)
        self.last_shoot = 0
        self.parent = parent
        self.ally = parent.ally
        if not hasattr(self, 'cooldown'):
            self.cooldown = 0

    def shoot(self, time, x, y, power=1):
        if self.parent.weapon_level > len(self.levels)-1:
            i = len(self.levels)-1
        else:
            i = self.parent.weapon_level
        has_shot = False
        for projectile in self.levels[i]:
            if time > self.last_shoot + projectile['cooldown']:
                proj = globals()[projectile['type']]
                projectile['initial_pos'] = (x, y)
                p = proj(self.scene, self.parent, projectile)
                p.charge = power
                p.add()
                has_shot = True
        if has_shot:
            self.last_shoot = time


class Visible(Actor):
    """actor with a surface"""
    def __init__(self, scene, params={}):
        Actor.__init__(self, scene, params)
        self.visible = True
        # load image of appropriate type (with collisions if has alpha)
        if not hasattr(self, 'has_alpha'):
            self.has_alpha = True
        if not hasattr(self, 'opacity'):
            self.opacity = 255
        if not hasattr(self, 'can_collide'):
            self.can_collide = True
        # start with surface corresponding 
        self.surface_name = self.name
        self.init_surface()
        # a list of childrens (following scene state changes)
        self.children = []
        # animation controler ?
        if not hasattr(self, 'animations'):
            self.animations = []
        else:
            for ani in self.animations:
                # a animation object to control surface
                targClass = globals()[ani['type']]
                self.children.append(targClass(self.scene, self, ani))
        if not hasattr(self, 'has_shadow'):
            self.has_shadow = False
        else:
            if self.has_shadow:
                self.children.append(Shadow(self.scene, self, parameters.SHADOW))

    def _get_surface(self):
        """surface is exported as pygame surface
        BUT set with an str in next function"""
        return self._surface

    def _set_surface(self, new_surface):
        """set pygame surface, collision array and hitmap
        according to newsurface (string of name or pygame surf)"""
        if isinstance(new_surface, str) or new_surface is None:
            if self.can_collide:
                maps = self.scene.cont.surf_alt(new_surface, self.has_alpha)
                # with alpha channel and collision array
                self._surface = maps[0]
                self.array = maps[1]
                self.hit = maps[2]
                self.shadow = maps[3]
            else:
                surf = self.scene.cont.surf_noalt(new_surface, self.has_alpha)
                self._surface = surf
            # remember alpha colorkey
            self.alpha_key = self._surface.get_colorkey()
            # keep new name
            self.surface_name = new_surface
        else:
            # modify actual surface
            self._surface = new_surface
        # remember opacity
        self._surface.set_alpha(self.opacity)
    surface = property(_get_surface, _set_surface)

    def init_surface(self):
        self.surface = self.surface_name

    def add(self):
        Actor.add(self)
        for ani in self.children:
            ani.add()

    def remove(self):
        Actor.remove(self)
        for ani in self.children:
            ani.remove()

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True


class Mobile(Visible):
    """a mobile sprite"""
    def __init__(self, scene, params={}):
        self._pos = (0, 0)
        Visible.__init__(self, scene, params)
        if not hasattr(self, 'speed'):
            self.speed = 0
        # the proportion of outside screen where mobile can subsist
        if not hasattr(self, 'margin_proportion'):
            self.margin_proportion = 1
        if not hasattr(self, 'trajectory'):
            self.trajectory = None
            self.movement = None
        else:
            # a trajectory object to control position
            trajClass = getattr(movement, self.trajectory)
            # does it have special parameters ?
            if 'trajectory_params' in params:
                self.movement = trajClass(self.scene, self,
                                          params['trajectory_params'])
            else:
                self.movement = trajClass(self.scene, self)

        self.base_surface = self.surface
        self.update_frame()
        if 'initial_pos' in params:
            self.center_on(params['initial_pos'])

    def remove(self):
        """remove from scene"""
        Visible.remove(self)
        try:
            del self.movement
        except AttributeError:
            pass

    def _get_pos(self):
        """world wants exact position"""
        position = int(self._pos[0]), int(self._pos[1])
        return position

    def _set_pos(self, new_position):
        self._pos = new_position[0], new_position[1]
    pos = property(_get_pos, _set_pos)

    def update_frame(self):
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.center = tools.get_center(self.pos, self.width, self.height)

    def move(self, interval, time):
        if self.trajectory is not None:
            self._pos = self.movement.next_pos(self._pos, interval, time)

    def center_on(self, target):
        """center self on another mobile or on x, y coordinates"""
        if hasattr(target, 'pos'):
            x, y = target._pos
            w, h = target.surface.get_width()/2., target.surface.get_height()/2.
            sw, sh = self.width/2., self.height/2.
            self._pos = x + w - sw, y + h - sh
        else:
            x, y = target
            sw, sh = self.width/2., self.height/2.
            self._pos = x - sw, y - sh

    def in_boundaries(self, pos, margin_proportion=0):
        # bad if outside screen and too far
        left_limit = - self.scene.limits[0] * margin_proportion
        right_limit = self.scene.limits[0] + self.scene.limits[0] * margin_proportion
        up_limit = - self.scene.limits[1] * margin_proportion
        down_limit = self.scene.limits[1] + self.scene.limits[1] * margin_proportion

        if (pos[0] > right_limit
            or pos[1] > down_limit
            or pos[0] + self.width < left_limit
            or pos[1] + self.height < up_limit):
            return False
        else:
            return True

    def update(self, interval, time):
        self.update_frame()
        self.move(interval, time)
        # delete if outside screen
        if not self.in_boundaries(self.pos, self.margin_proportion):
            self.remove()
            del self


class Anim(Actor):
    """basic animation actor
    when added in scene it changes its parent surface"""
    def __init__(self, scene, parent, params={}):
        Actor.__init__(self, scene, params)
        self.parent = parent
        # appearance should be updated late
        self.priority = parameters.ANIMPRIOR


class Film(Anim):
    """when added launches serie of sprites 
    each with same given duration
    then disappears
    """
    def __init__(self, scene, parent, params={}):
        Anim.__init__(self, scene, parent, params)
        self.nb_frames = len(self.sprites)
        self.parent = parent
        if  not hasattr(self, 'to_nothing'):
            self.to_nothing = False

    def update(self, interval, time):
        still_up = False
        # accordin to time select right sprite or remove
        for i in range(self.nb_frames):
            if self.init_time + i * self.pulse <= time < self.init_time + (i+1) * self.pulse:
                self.parent.surface = self.sprites[i]
                still_up = True
                break
        if not still_up:
                if self.to_nothing:
                    self.parent.init_surface()
                    self.parent.remove()
                self.remove()


class Loop(Film):
    def __init__(self, scene, parent, params):
        Film.__init__(self, scene, parent, params)
        self.state = 0
        self.cumul = 0

    def update(self, interval, time):
        # select next sprite ?
        if self.cumul + interval > self.durations[self.state]:
            self.cumul = 0
            # change appearance of animated parent
            self.parent.surface = self.sprites[self.state]
            # if reaching last frame, restart
            if self.state + 1 > self.nb_frames-1:
                self.state = 0
            else:
                self.state += 1
        else:
            self.cumul += interval


class SyncLoop(Film):
    """This looping anim is relative to the time of the scene
    so that anims with same durations are in sync"""
    def __init__(self, scene, parent, params):
        Film.__init__(self, scene, parent, params)
        self.cumul_dur = [0]
        for d in self.durations:
            self.cumul_dur.append(d + self.cumul_dur[-1])
        self.total_dur = self.cumul_dur[-1]
        self.cumul_dur = self.cumul_dur[:-1]

    def update(self, interval, time):
        # sync durations of anim and time
        repeat = int(time / self.total_dur)
        sync_time = time - repeat * self.total_dur
        # select right sprite
        for i in range(self.nb_frames-1, -1, -1):
            if sync_time > self.cumul_dur[i]:
                self.parent.surface = self.sprites[i]
                break


class Blank(Anim):
    def update(self, interval, time):
        # accordin to time select blank sprite
        if time <= self.init_time + self.duration:
            self.parent.surface = self.parent.hit
        else:
            self.parent.init_surface()
            self.remove()


class Roll(Anim):
    """change surface according to direction
    needs 3 sprites"""
    def __init__(self, scene, parent, params={}):
        Anim.__init__(self, scene, parent, params)
        self.parent = parent
        self.player = self.parent.player
        self.base_name = self.parent.name
        # ref for animation of ship movements
        self.last_bend = 0
        self.righto = False
        self.lefto = False

    def update(self, interval, time):
        # detect change of direction
        if self.player.go_right and not self.righto:
            self.righto = True
            self.lefto = False
            self.last_bend = time
        elif self.player.go_left and not self.lefto:
            self.lefto = True
            self.righto = False
            self.last_bend = time
        # show orientation of ship
        if self.player.go_right and time > self.last_bend + self.delay:
            self.parent.surface = self.sprites[0]
        elif self.player.go_left  and time > self.last_bend + self.delay:
            self.parent.surface = self.sprites[2]
        else:
            self.parent.surface = self.sprites[1]

class EightDir(Anim):
    """change surface according to direction toward target"""
    def __init__(self, scene, parent, params={}):
        Anim.__init__(self, scene, parent, params)
        self.parent = parent
        self.current = 0
        #prepare animations instances
        self.anim_instances = []
        for ani in self.animations:
            targClass = globals()[ani['type']]
            instance = targClass(self.scene, self.parent, ani)
            self.anim_instances.append(instance)
        self.last_change = 0
    
    def replace_anim(self, new_direction):
        '''replace current animation of parent'''
        # the parameters
        ani = self.animations[new_direction]
        # the instanciation of the one dir anim
        instance = self.anim_instances[new_direction]
        # remove precedent anim
        for i in self.parent.children:
            if i in self.anim_instances:
                i.remove()
                self.parent.children.remove(i)
        
        self.parent.children.append(instance)        
        instance.add()
    
    def sprite_from_angle(self, angle):
        """align with sprite order"""
        angle += 90
        i = angle / 360. * 8
        return int(round(i))

    def update(self, interval, time):
        #try to find a target
        self.target = self.search_enemy(time)
        #aim at it
        angle = self.aim_angle()
        new_direction = self.sprite_from_angle(angle)
        # update appearance every 100ms
        if time > self.last_change + 100:
            if new_direction != self.current:
                self.replace_anim(new_direction)
                self.current = new_direction
                self.last_change = time

class Projectile(Mobile):
    """projectile positions should be accessed with position(index)
    damage
    """
    def __init__(self, scene, parent, params={}):
        # projectiles shouldn't exist outside screen
        self.margin_proportion = 0
        self.parent = parent
        Mobile.__init__(self, scene, params)
        self.ally = parent.ally
        self.center_offset = self.width/2, self.height/2
        # how a projectile can be collided
        if not hasattr(self, 'collision_type'):
            self.collision_type = 'pixel_perfect'
        # how does it affect life
        if not hasattr(self, 'effect'):
            self.add_life = -1
        else:
            if 'add_life' not in self.effect:
                self.add_life = -1
            else:
                self.add_life = self.effect['add_life']

    def collided(self, projectile, time):
        self.remove()

    def get_damage(self):
        return self.add_life


class Bullet(Projectile):
    pass

class LineBullet(Projectile):
    def __init__(self, scene, parent, params={}):
        Projectile.__init__(self, scene, parent, params)
        # define target
        self.target = self.search_enemy()
        a = self.aim_angle()
        # move toward enemy position at shooting time
        self.movement = movement.Line(self.scene, self, {'angle': a})


class Missile(Projectile):
    def __init__(self, scene, parent, params={}):
        # initialize projectile
        Projectile.__init__(self, scene, parent, params)
        # define missile target
        self.target = None
        self.launch_time = scene.now
        min_target_count = 10000000
        for item in scene.content:
            if not item.ally and hasattr(item, 'life'):
                # add actor to the targeting system
                if not hasattr(item, 'is_target'):
                    item.is_target = 0
                # target the actor if not already targeted
                if item.is_target == 0:
                    self.target = item
                    break
                # otherwise, target the least targeted actor
                elif item.is_target < min_target_count:
                    self.target = item
                    min_target_count = item.is_target
        if self.target is not None:
            self.target.is_target += 1
        # custom offset
        params['initial_pos'] = (params['initial_pos'][0]+4, params['initial_pos'][1]+5)
        
        self.max_speed = self.speed  # missile has to accelerate
        self.speed = 0.01  # initial speed
        self.acceleration = 0.0003  # pixels per square millisecond

        # save 'targeted' trajectory for later use
        self.targeted_trajectory = self.movement

        # set initial
        self.movement = movement.Line(self.scene, self, {'angle': 90})
        self.primary_trajectory = True

        # add crosshair
        if hasattr(self.target, 'life'):
            self.crosshair = Follower(scene, self.target, {'name': 'crosshair'})
            self.crosshair.add()

    def remove(self):
        Projectile.remove(self)
        try:
            self.crosshair.remove()
        except AttributeError:
            pass

    def update(self, interval, time):
        Projectile.update(self, interval, time)
        self.speed = movement.accelerate(self.speed, self.max_speed, self.acceleration, interval)
        if (self.target is None) or self.target.life <= 0:
            try:
                self.crosshair.remove()
            except AttributeError:
                pass
        if (hasattr(self, 'movement') and self.primary_trajectory
                and self.scene.now - self.launch_time > 150):
            self.movement = self.targeted_trajectory
            self.primary_trajectory = False
            del self.targeted_trajectory


class Blast(Projectile):
    """charged shots
    power
    """
    def __init__(self, scene, parent, params={}):
        Projectile.__init__(self, scene, parent, params)
        self.charge = 0

    def collided(self, projectile, time):
        pass

    def get_damage(self):
        # get power of charged shot
        amount = self.charge * self.power
        return amount


class Landscape(Visible):
    """a scrolling background
    (not moving but looping)
    """
    def __init__(self, scene, params={}):
        self.can_collide = False
        Visible.__init__(self, scene, params)
        if  not hasattr(self,'speed'):
            self.speed = 0
        self.full = self.surface
        self.width, self.height = self.full.get_size()
        self.offset = self.height

    def update(self, interval, time):
        # move down the displayed area of landscape
        self.offset -= self.speed * interval

        w, h = self.width, parameters.GAMESIZE[1]
        # do not loop if smaller than screen background
        if self.height >= h:
            # loop background
            if self.offset < 0:
                self.offset = self.height
            if self.offset + h > self.height:
                t1 = self.offset
                h1 = self.height - self.offset
                h2 = h - (self.height - self.offset)
                if self.has_alpha:
                    back = tools.make_rect(w, h, self.alpha_key)
                    s1 = self.full.subsurface(0, t1, w, h1)
                    s2 = self.full.subsurface(0, 0, w, h2)
                    s1.set_alpha(255)
                    s2.set_alpha(255)
                    s = tools.compose_surfaces(w, h, s1, s2, back)

                    s.set_colorkey(self.alpha_key)
                    s.set_alpha(self.opacity)
                else:
                    s1 = self.full.subsurface(0, t1, w, h1)
                    s2 = self.full.subsurface(0, 0, w, h2)

                    s = tools.compose_surfaces(w, h, s1, s2)
            else:
                s = self.full.subsurface(0, self.offset, w, h)
        else:
            s = self.full
        self.surface = s


class Catchable(Mobile):
    """this one you can catch
    parameters should contain:
    -'effect'
    """
    def __init__(self, scene, params):
        Mobile.__init__(self, scene, params)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # how does it affect life
        if 'add_life' not in self.effect:
            self.add_life = 0
        else:
            self.add_life = self.effect['add_life']
        # how does it affect weapons
        if 'upgrade_weapon' not in self.effect:
            self.weapon_bonus = 0
        else:
            self.weapon_bonus = self.effect['upgrade_weapon']

    # what happens when it collides with another object
    def collided(self, projectile, time):
        self.remove()

    # return quantity of heal (or damage)
    def get_damage(self):
        return self.add_life

    # return upgrade power
    def upgrade_weapon(self):
        return self.weapon_bonus


class Fragile(Mobile):
    """this one can be hurt
    parameters should contain:
    -life
    """
    def __init__(self, scene, params):
        Mobile.__init__(self, scene, params)
        self.killer = None
        self.last_hit = 0
        self.time_of_death = None
        # cannot leave bonus when death by default
        if not hasattr(self, 'bonus_rate'):
            self.bonus_rate = 0
        # reward for killing
        if not hasattr(self, 'reward'):
            self.reward = 0
        # how a fragile can be collided
        if not hasattr(self, 'collision_type'):
            self.collision_type = 'pixel_perfect'
        # fragile has hit_anim
        self.hit_anim = Blank(self.scene, self, parameters.HITBLINK)
        # fragile can explode
        self.end = Mobile(self.scene, parameters.EXPLOSION)
        # fragiles can give bonuses depending on their bonus rate
        if random.random() < self.bonus_rate:
            self.has_bonus = True
            if random.random() < parameters.DEFAULTPLAY['ratio_life_upgrade']:
                self.bonus = Catchable(self.scene, parameters.BONUSWEAPON)
            else:
                self.bonus = Catchable(self.scene, parameters.BONUSLIFE)
        else:
            self.has_bonus = False
        # prepare score show if significant
        if self.reward > 0 and not self.ally:
            self.rew = Desc(self.scene, self, str(self.reward))

    def collided(self, projectile, time):
        # persistent projectiles have damage pulse
        if time - self.last_hit > self.scene.gameplay['hit_pulse']:
            self.last_hit = time
            # heal or take damage
            self.life += projectile.get_damage()
            if self.life <= 0:
                self.time_of_death = time
                # recognize killer in the distance
                if hasattr(projectile, 'parent'):
                    self.killer = projectile.parent
                # close combat killing
                else:
                    self.killer = projectile

    def get_damage(self):
        return parameters.COLLISIONDAMAGE

    def die(self):
        # remove of scene
        self.remove()
        # reward shooter
        self.killer.score += self.reward

        if self.has_bonus:
            # the bonus will appear where the non ally died
            self.bonus.center_on(self)
            # add a bonus in scene
            self.bonus.add()
        if self.reward > 0:
            # show reward
            self.rew.add()
        # explode
        self.end.center_on(self)
        self.end.add()
        # play explosion sound at correct stereo position
        self.scene.cont.play('explosion', self.pos[0])

    def update(self, interval, time):
        Mobile.update(self, interval, time)
        # change color for some time if hit recently
        if time < self.last_hit + self.hit_anim.duration:
            self.hit_anim.add()
            # ~ self.surface = self.scene.cont.hit[self.name]
        if self.life <= 0:
            self.die()


class Fighter(Fragile):
    """a shooting mobile sprite"""
    def __init__(self, scene, params):
        Fragile.__init__(self, scene, params)
        self.last_shoot = 0
        self.arms = {}
        # instantiate weaponz
        if 'weapons' in params:
            for weapon in params['weapons']:
                self.new_weapon(weapon)
        self.score = 0
        # ref to upgrade_weapon
        self.weapon_level = 0

    def new_weapon(self, params):
        # instanciate weapon
        w = Weapon(self.scene, self, params)
        # set map allied status
        w.ally = self.ally
        # keep trace of weapon
        self.arms.update({params['name']: w})

    def shoot(self, time, x, y):
        for name in self.arms:
            self.arms[name].shoot(time, x, y)

    def update(self, interval, time):
        Fragile.update(self, interval, time)
        # autofire
        x, y = (self.center[0], self.center[1])
        self.shoot(time, x, y)


class ChargeFighter(Fighter):
    """a charging mobile sprite
    charge_rate"""
    def __init__(self, scene, params):
        Fighter.__init__(self, scene, params)
        self.charge = 0.
        # can have a charge display following fighter
        # ~ self.aura = Charge(self.scene, self)

    def add(self):
        Fighter.add(self)
        # ~ self.aura.add()

    # ~ def shoot(self, time, weapon, power=None):
        # ~ w = self.arms[weapon]
        # ~ # most projectiles aren't charged
        # ~ if weapon == 'Bullet':
            # ~ # limit fire rate and stop when charging
            # ~ if (time > self.last_shoot + w.cooldown
            # ~ and self.charge == 0 ):
                # ~ x, y = (self.center[0], self.center[1])
                # ~ w.shoot(x, y)
                # ~ self.scene.cont.play('shoot', self.pos[0])
                # ~ self.last_shoot = time
        # ~ # blast shot
        # ~ elif weapon == 'Blast':
            # ~ x, y = (self.center[0], self.center[1])
            # ~ w.shoot(x, y, power)

    def die(self):
        Fighter.die(self)
        # remove also charge display
        # ~ self.aura.remove()


class Ship(ChargeFighter):
    """A ship controlled by player and shooting"""
    def __init__(self, scene, player, params):
        ChargeFighter.__init__(self, scene, params)
        self.player = player
        # keep ref of maximum life
        self.max_life = self.life
        # ship has orientation_anim
        self.children.append(Roll(self.scene, self, parameters.SHIPORIENTATION))
        self.layer = parameters.SHIPLAY
        self.scene.game.bind_control_switch('shield', self.player.index, self)

    def trigger(self, control):
        if control['name'] == 'shield':
            if self.player.keys['shield']:
                m = 'Shield Activated'
            if not self.player.keys['shield']:
                m = 'Shield Deactivated'

    def fly(self, direction, interval):
        # should consider time passed
        offset = self.speed * interval
        if direction == 'right':
            new_pos = self._pos[0]+offset, self._pos[1]
        elif direction == 'left':
            new_pos = self._pos[0]-offset, self._pos[1]
        elif direction == 'up':
            new_pos = self._pos[0], self._pos[1]-offset
        elif direction == 'down':
            new_pos = self._pos[0], self._pos[1]+offset
        new_center = tools.get_center(new_pos, self.width, self.height)
        # do not step outside screen
        if (0 <= new_center[0] <= self.scene.limits[0]
                and 0 <= new_center[1] <= self.scene.limits[1]):
            self._pos = new_pos
        else:
            # stick on border
            new_center = list(new_center)
            if new_center[0] > self.scene.limits[0]:
                new_center[0] = self.scene.limits[0]
            if new_center[0] < 0:
                new_center[0] = 0
            if new_center[1] > self.scene.limits[1]:
                new_center[1] = self.scene.limits[1]
            if new_center[1] < 0:
                new_center[1] = 0

            self._pos = tools.get_pos_from_center(new_center, self.width, self.height)

    def collided(self, projectile, time):
        ChargeFighter.collided(self, projectile, time)
        # can upgrade weapon when catching bonuses
        if isinstance(projectile, Catchable):
            self.weapon_level += projectile.upgrade_weapon()

    def die(self):
        ChargeFighter.die(self)
        # player is dead
        self.player.alive = False


class Follower(Mobile):
    """a sprite following another"""
    def __init__(self, scene, parent, params):
        Mobile.__init__(self, scene, params)
        if  not hasattr(self, 'offset'):
            self.offset = 0, 0
        self.parent = parent
        self.center_on(self.parent)
        # should be updated after parents
        self.priority = parameters.FOLLOWPRIOR

    def move(self, interval, time):
        """move to be centered on parent"""
        self.center_on(self.parent)
        self._pos = self._pos[0]+self.offset[0], self._pos[1]+self.offset[1]


class Shadow(Follower):
    def __init__(self, scene, parent, params):
        Follower.__init__(self, scene, parent, params)
        self.surface = self.parent.shadow

    def update(self, interval, time):
        Follower.update(self, interval, time)
        self.surface = self.parent.shadow


class Charge(Follower):
    """showing the charge of ship"""
    def __init__(self, scene, parent, offset=(0, 0)):
        # offset to show over ship
        Follower.__init__(self, scene, parent, offset)
        self.levels = [self.scene.cont.surf(' '),
        self.scene.cont.surf('B'),
        self.scene.cont.surf('BB'),
        self.scene.cont.surf('BBB')]
        # draw over background but under ship
        self.layer = parameters.BELOWSHIPLAY

    def update(self, interval, time):
        if self.parent.charge >= 1:
            self.surface = self.levels[3]
        elif self.parent.charge > 0.5:
            self.surface = self.levels[2]
        elif self.parent.charge > 0:
            self.surface = self.levels[1]
        elif self.parent.charge == 0:
            self.surface = self.levels[0]
        # center on parent at the end of update
        Follower.update(self, interval, time)


class Desc(Mobile):
    """showing descriptor on item"""
    def __init__(self, scene, parent, text='100', duration=500):
        Mobile.__init__(self, scene)
        self.parent = parent
        self.surface = self.scene.cont.surf(text)
        self.duration = duration
        self.layer = parameters.FRONTLAY

    def update(self, interval, time):
        if time > self.parent.time_of_death + self.duration:
            self.remove()
        self.center_on(self.parent)


class Widget(Mobile):
    def __init__(self, scene, path, params, offset=(0, 0)):
        Mobile.__init__(self, scene)
        # the widget shows content of object defined by path
        self.path = path
        self.params = params
        self.offset = offset
        self.value = self.new_value()
        self.surface = self.skin(self.value)
        self.shape = self.surface.get_width(), self.surface.get_height()
        self.pos = (0, 0)
        self.align()
        # support delayed updates
        if 'low_flip' in self.params:
            self.low = True
            self.last_flip = 0
        else:
            self.low = False
        # draw interface over rest of scene
        self.layer = parameters.INTERFACELAY

    def new_value(self):
        """gets a value deep in scene"""
        return getattr_deep(self.scene, self.path)

    def align(self):
        # recompute coordinates
        if 'center' in self.params:
            self.pos = (self.scene.limits[0]/2-self.shape[0]/2+self.offset[0],
                        self.scene.limits[1]/2-self.shape[1]/2+self.offset[1])
        if 'left' in self.params:
            self.pos = (self.offset[0], self.pos[1]+self.offset[1])
        if 'right' in self.params:
            self.pos = (self.scene.limits[0]-self.shape[0]+self.offset[0],
                        self.pos[1]+self.offset[1])
        if 'top' in self.params:
            self.pos = (self.pos[0]+self.offset[0], self.offset[1])
        if 'bottom' in self.params:
            self.pos = (self.pos[0]+self.offset[0],
                        self.scene.limits[1]-self.shape[1]+self.offset[1])

    def skin(self, value):
        surface = self.scene.sfont.render(str(int(value)), False,
                                          self.scene.theme['txt_color'])
        return surface

    def update(self, interval, time):
        # recompute surface
        new_value = self.new_value()
        if not self.low:
            if self.value != new_value:
                self.value = new_value
                self.surface = self.skin(new_value)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape:
                    self.shape = new_shape
                    self.align()
        else:
            if time > self.last_flip + 500 and self.value != new_value:
                self.value = new_value
                self.last_flip = time
                self.surface = self.skin(new_value)
                new_shape = self.surface.get_width(), self.surface.get_height()
                if self.shape != new_shape:
                    self.shape = new_shape
                    self.align()


class Score(Widget):
    """shows score of player (id given by path)"""
    def new_value(self):
        player = self.scene.players[self.path]
        # complete with leading zeros
        score = int(player.score)
        return score

    def skin(self, value):
        value = str(value).rjust(5, '0')
        surface = self.scene.sfont.render(value, False,
        self.scene.theme['txt_color'])
        return surface


class Life(Widget):
    """shows life bar of player (id given by path)"""
    def new_value(self):
        player = self.scene.players[self.path]
        return float(player.life) / player.max_life

    def skin(self, value):
        # load back sprite of life bar
        back = self.scene.cont.surf('_____')
        front = self.scene.cont.surf('+++++')
        w = front.get_width()
        h = front.get_height()
        size = int(w * value)
        # blit only a portion of life bar
        surf = tools.blit_clip(front, back, (0, 0, size, h))
        return surf
