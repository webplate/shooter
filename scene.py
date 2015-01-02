# !/usr/bin/env python
# -*- coding: utf-8 -*-
import entity, tools, parameters
import numpy
import pygame.locals as p_l


class Player():
    """class for player settings, controls, ships"""
    def __init__(self, scene, index):
        self.scene = scene
        self.index = index

        # create control state list
        self.keys = self.scene.game.controller.controls_state[index]

        self.go = {}
        self.go.update({'up': False})
        self.go.update({'down': False})
        self.go.update({'left': False})
        self.go.update({'right': False})
        self.stop = True

        self.settings = {}
        self.ship = None
        self.latent = None
        self.alive = False
        self.active = False
        self.score = 0
        self.life = 0
        self.max_life = 1

    def trigger(self, control):
        # join game
        if control['name'] == 'new_player' and self.ship is None:
            # summon in scene
            self.alive = True  # False when ship dies
            self.active = True  # Remains True !
            if self.latent is None:
                self.latent = self.load_ship(self.settings['ship'])
            self.ship = self.latent
            self.ship.add()
            self.scene.game.controller.unbind_control('new_player', self.index, self)
            self.scene.game.controller.bind_control_switch('up', self.index, self)
            self.scene.game.controller.bind_control_switch('down', self.index, self)
            self.scene.game.controller.bind_control_switch('left', self.index, self)
            self.scene.game.controller.bind_control_switch('right', self.index, self)
            self.scene.game.controller.bind_control_switch('shoot', self.index, self)

        # ship control events
        elif control['name'] in ['up', 'down', 'left', 'right']:
            axes = (('up', 'down'), ('left', 'right'))
            for axis in axes:
                if control['name'] in axis:
                    # joystick event
                    if control['event_type'] == p_l.JOYAXISMOTION:
                        value = control['event_params']['value']
                        tol = control['event_params']['tol']
                        direction = control['event_params']['direction']
                        if value > tol:
                            self.keys[axis[0]] = False
                        elif value < tol and direction == 'negative':
                            self.keys[axis[0]] = True
                        if value < tol:
                            self.keys[axis[1]] = False
                        elif value > tol and direction == 'positive':
                            self.keys[axis[1]] = True

                    # change movement flags accordingly
                    if self.keys[axis[0]] and not self.go[axis[0]] and not self.keys[axis[1]]:
                        self.go[axis[0]] = True
                        self.stop = False
                    elif not self.keys[axis[0]] and self.go[axis[0]]:
                        self.go[axis[0]] = False
                    if self.keys[axis[1]] and not self.go[axis[1]] and not self.keys[axis[0]]:
                        self.go[axis[1]] = True
                        self.stop = False
                    elif not self.keys[axis[1]] and self.go[axis[1]]:
                        self.go[axis[1]] = False

    def load_ship(self, parameters):
        # instantiate according to specified type
        targetClass = getattr(entity, parameters['type'])
        ship = targetClass(self.scene, self, parameters)
        # init position
        coord = (self.scene.limits[0]/2,
        self.scene.limits[1]-self.scene.limits[1]/6)
        ship.pos = coord
        # link to ship attributes
        self.life = ship.life
        self.score = ship.score
        self.weapon_level = ship.weapon_level
        return ship

    def command(self, interval, time):
        """command ship !!"""
        if self.go['right']:
            self.ship.fly('right', interval)
        elif self.go['left']:
            self.ship.fly('left', interval)
        if self.go['up']:
            self.ship.fly('up', interval)
        elif self.go['down']:
            self.ship.fly('down', interval)
        # is the ship charging ?
        if self.keys['shoot']:
            offset = self.ship.charge_rate * interval
            if self.ship.charge + offset > 1:
                self.ship.charge = 1.
            else:
                self.ship.charge += offset
        else:
            # charged shot
            if self.ship.charge > 0.5:
                self.ship.shoot(time, 'Blast', self.ship.charge)
            self.ship.charge = 0.

    def update(self, interval, time):
        if self.alive:
            self.command(interval, time)
        # update info from ship if it exists
        if self.ship is not None:
            self.life = self.ship.life
            self.max_life = self.ship.max_life
            self.score = self.ship.score


class Container():
    """stock surfaces and projectiles maps to prevent duplicates
    stock sounds also
    """
    def __init__(self, scene):
        self.scene = scene
        self.theme = {}
        self.surfaces = {}
        self.array = {}
        self.hit = {}
        self.shadow = {}
        self.maps = {}
        self.background = {}
        self.pmap = {}
        self.snds = {}

    def create_all(self, name, alpha=True):
        """generate surface and alternative maps
        and reference them"""
        surface = tools.load_image(name, self.theme, self.scene, alpha)
        self.surfaces.update({name: surface})
        hit = tools.make_white(surface)
        shadow = tools.make_shadow(surface, parameters.SHADOWSCALE)
        array = tools.make_array(surface)
        self.hit.update({name: hit})
        self.shadow.update({name: shadow})
        self.array.update({name: array})
    
    def create_surf(self, name, alpha=True):
        """generate only pygame surface """
        surface = tools.load_image(name, self.theme, self.scene, alpha)
        self.surfaces.update({name: surface})

    def surf(self, name):
        """avoid duplicate loading"""
        # None is the empty surface
        if name is None:
            name = ''
        if name not in self.surfaces:
            # generate also variants of image
            self.create_all(name)
        surface = self.surfaces[name]
        return surface
    
    def surf_alt(self, name, alpha=True):
        """return alt maps too"""
        # None is the empty surface
        if name is None:
            name = ''
        if name not in self.surfaces:
            self.create_all(name, alpha)
        surface = self.surfaces[name]
        array = self.array[name]
        hit = self.hit[name]
        shadow = self.shadow[name]
        return surface, array, hit, shadow
        
    def surf_noalt(self, name, alpha=True):
        """generate and return only pygame surface"""
        # None is the empty surface
        if name is None:
            name = ''
        if name not in self.surfaces:
            self.create_surf(name, alpha)
        surface = self.surfaces[name]
        return surface

    def snd(self, name):
        """load sounds"""
        if name in self.snds:
            sound = self.snds[name]
        else:
            sound = tools.load_sound(name, self.scene)
            self.snds.update({name: sound})
        return sound

    def play(self, sound, xpos):
        p = (self.scene.limits[0] - abs(xpos)) / float(self.scene.limits[0])
        # adjust volume
        p = p * self.scene.snd_pack['effect_volume']
        if not self.scene.mute:
            sound = self.snd(sound)
            if sound is not None:
                channel = sound.play()
                channel.set_volume(p, 1-p)

    def load_music(self, track=None, loops=-1):
        if not self.scene.game.no_sound:
            if track is not None:
                music = tools.load_stream(track, self.scene)
                # check if file is nicely loaded
                if music:
                    self.scene.game.music.play(loops)
                    self.scene.game.music.set_volume(self.scene.snd_pack['music_volume'])
                    self.music()

    def music(self):
        """control game mixer for streaming large music files"""
        if (not self.scene.mute and not self.scene.paused
                and not self.scene.game.no_sound):
            self.scene.game.music.unpause()
        else:
            self.scene.game.music.pause()


class Ordered():
    """stock objects of scene in layered priority
    """
    def __init__(self):
        self.content = [[]]

    def __iter__(self):
        """a generator to emit content in right order"""
        for group in self.content:
            for item in group:
                yield item

    def append(self, item, priority=0):
        """update size of container dynamically"""
        while len(self.content) <= priority:
            self.content.append([])
        self.content[priority].append(item)

    def remove(self, item):
        """remove item from content"""
        for group in self.content:
            if item in group:
                group.remove(item)

    def prioritize(self, item, priority):
        """reorder an item in a specific layer of priority
        or add a new item"""
        # eliminate prior version
        self.remove(item)
        # insert with new priority
        self.append(item, priority)


class Scene():
    def __init__(self, game):
        self.game = game
        # delay between scene and game (scene can be paused)
        self.delay = 0
        self.now = 0
        self.paused = False
        self.mute = True
        self.limits = game.limits
        self.font = game.font
        self.mfont = game.mfont
        self.sfont = game.sfont
        # create four players
        self.players = [Player(self, i) for i in range(4)]
        # no level loaded yet
        self.level = None
        # an object for efficient loading
        self.cont = Container(self)
        # content in priority update order
        self.content = Ordered()
        # create en empty sprite container
        self.lst_sprites = Ordered()

        # show menu at start
        self.update = self.update_menu
        self.in_menu = True

        # controller configuration
        self.game.controller.toggle_active_controls('global', True)
        self.game.controller.toggle_active_controls('menu', True)
        self.game.controller.bind_control('menu', -1, self)
        self.game.controller.bind_control('pause', -1, self)
        self.game.controller.bind_control('mute', -1, self)

    def trigger(self, control):
        # change level command
        if control['name'] == 'change_level':
            level = parameters.LEVEL
            level = tools.fill_dict_with_default(level, parameters.DEFAULTLEVEL)
            self.play_level(level)
        # pause command
        elif control['name'] == 'pause':
            if not self.paused:
                self.game.controller.toggle_active_controls('game', False)
                self.pause(self.game.now * self.game.speed)
                self.update = self.update_paused
            else:
                self.game.controller.toggle_active_controls('game', True)
                self.unpause(self.game.now * self.game.speed)
                self.update = self.update_level
        # menu command
        elif control['name'] == 'menu':
            if not self.in_menu:
                # open menu if it is closed
                if not self.paused:
                    self.trigger({'name': 'pause'})
                self.game.controller.toggle_active_controls('pause', False)
                self.game.controller.toggle_active_controls('menu', True)
                self.game.menu.trigger({'name': 'open_menu'})
                self.update = self.update_menu
                self.in_menu = True
            elif self.level is not None:
                # close menu if it is open and a level is loaded
                if self.paused:
                    self.trigger({'name': 'pause'})
                self.game.controller.toggle_active_controls('pause', True)
                self.game.controller.toggle_active_controls('menu', False)
                self.in_menu = False
        # mute command
        elif control['name'] == 'mute':
            if not self.mute:
                self.mute = True
            else:
                self.mute = False
        # scene can receive 'new_player' from an unassigned joystick
        elif control['name'] == 'new_player':
            for player in range(3):
                if not self.players[player].active:
                    self.game.joysticks[-1].remove(control['event_params']['joy'])
                    self.game.joysticks[player].append(control['event_params']['joy'])
                    self.players[player].trigger(control)
                    break

    def play_level(self, level):
        self.level = level
        self.theme = self.level['theme']
        self.cont.theme = self.theme['name']
        self.snd_pack = self.level['sound_pack']
        self.gameplay = self.level['gameplay']

        # unbind players controls
        for player in range(4):
            self.game.controller.unbind_player(player)
        # reset players
        self.players = [Player(self, i) for i in range(4)]
        # reset scene content
        self.content = Ordered()
        # reset delay
        self.delay = 0

        # player settings from loaded level and bind 'new_player' controls
        for player in self.players:
            player.settings.update(self.level['player'])
            self.game.controller.bind_control('new_player', player.index, player)
        self.game.controller.bind_control('new_player', -1, self)

        # load game interface
        self.load_interface()

        # launch background music
        self.cont.load_music(self.level['music'])
        # launch landscape
        entity.Landscape(self, self.level['background']).add()
        entity.Landscape(self, parameters.CLOUD).add()
        # change active controls and reroute update function
        self.update = self.update_level
        self.in_menu = False
        self.paused = False
        self.game.controller.toggle_active_controls('menu', False)
        self.game.controller.toggle_active_controls('game', True)
        self.game.controller.toggle_active_controls('pause', True)
        self.update()

    def load_interface(self):
        # interface
        self.interface = [
            entity.Life(self, 0, ['bottom', 'left']),
            entity.Score(self, 0, ['bottom', 'left'], (0, -10)),
            entity.Life(self, 1, ['bottom', 'right']),
            entity.Score(self, 1, ['bottom', 'right'], (0, -10)),
            entity.Life(self, 2, ['bottom', 'left'], (30, 0)),
            entity.Score(self, 2, ['bottom', 'left'], (30, -10)),
            entity.Life(self, 3, ['bottom', 'right'], (-30, 0)),
            entity.Score(self, 3, ['bottom', 'right'], (-30, -10)),
            entity.Widget(self, 'game.fps', ['bottom', 'right', 'low_flip'], (0, -30))
        ]
        
        # add in scene
        for item in self.interface:
            item.add()

    def collide(self, proj_map, target_map, time):
        """repercute collisions projectiles and alpha maps of sprites
        dealing with projectiles as entities (entity.Mobile)"""
        for xP, yP, xPe, yPe, itemP in proj_map:
            # one pixel projectile
            if itemP.collision_type == 'pixel':
                # focus on center_pixel
                xP, yP = itemP.center
                for xT, yT, xTe, yTe, itemT in target_map:
                    # is in range ?
                    if xT < xP < xTe and yT < yP < yTe:
                        # per pixel collision
                        if self.cont.array[itemT.name][xP - xT, yP - yT]:
                            # hurt or not, entity
                            itemT.collided(itemP, time)
                            # remove or not, colliding projectile
                            itemP.collided(itemT, time)
            # rectangular projectile
            elif itemP.collision_type == 'rectangle':
                for xT, yT, xTe, yTe, itemT in target_map:
                    if xP <= xTe and xPe >= xT and yP <= yTe and yPe >= yT:
                        # (minx,miny), (maxx, maxy) are the intersection
                        # coordinate between target map and proj map
                        # coordinate are target map relative
                        minx, maxx = max(xP, xT)-xT, min(xPe, xTe)-xT
                        miny, maxy = max(yP, yT)-yT, min(yPe, yTe)-yT
                        if True in self.cont.array[itemT.name][minx:maxx, miny:maxy]:
                            itemT.collided(itemP, time)
                            itemP.collided(itemT, time)
            # pixel perfect projectile
            else:
                for xT, yT, xTe, yTe, itemT in target_map:
                    if xP <= xTe and xPe >= xT and yP <= yTe and yPe >= yT:
                        minx, maxx = max(xP, xT)-xT, min(xPe, xTe)-xT
                        miny, maxy = max(yP, yT)-yT, min(yPe, yTe)-yT
                        minxP, maxxP = max(xP, xT)-xP, min(xPe, xTe)-xP
                        minyP, maxyP = max(yP, yT)-yP, min(yPe, yTe)-yP
                        touch = numpy.logical_and(
                            self.cont.array[itemT.name][minx:maxx, miny:maxy],
                            self.cont.array[itemP.name][minxP:maxxP, minyP:maxyP])
                        if True in touch:
                            itemT.collided(itemP, time)
                            itemP.collided(itemT, time)

    def pause(self, time):
        self.paused = True
        self.pause_time = time

    def unpause(self, time):
        self.paused = False
        self.delay += time - self.pause_time

    def add_sprite(self, x, y, item):
        """update sprite container only for visible objects"""
        if item.visible:
            identifier = ((x, y), item.surface)
            self.lst_sprites.append(identifier, item.layer)

    def update_menu(self, interval=0, time=0):
        # keep sprites from the game to make background image
        self.game_sprites = self.lst_sprites.content[:parameters.INTERFACELAY+1]
        self.lst_sprites = Ordered()
        self.lst_sprites.content = self.game_sprites
        # stop background music
        self.cont.music()
        # update menu and get menu sprites
        self.game.menu.update()
        self.game.menu.add_sprites(self.game.menu.active_menu)

    def update_paused(self, interval=0, time=0):
        # stop background music
        self.cont.music()
        # add "PAUSE" string
        surf = self.font.render('PAUSE', True, (140, 200, 0))
        surf2 = self.font.render('PAUSE', True, (0, 0, 0))
        x = parameters.GAMESIZE[0] / 2 - surf.get_width() / 2
        y = parameters.GAMESIZE[1] / 2 - surf.get_height() / 2
        identifier = ((x, y), surf)
        identifier2 = ((x+1, y+1), surf2)
        self.lst_sprites.append(identifier2, parameters.MESSAGELAY)
        self.lst_sprites.append(identifier, parameters.MESSAGELAY)

    def update_level(self, interval=0, time=0):
        self.now = time - self.delay
        # collision maps
        ship_map = []
        target_map = []
        ship_proj_map = []
        ship_blast_map = []
        target_proj_map = []
        bonus_map = []
        # reset sprite list for drawing
        self.lst_sprites = Ordered()
        self.nb_fighters = 0
        # explore scene
        # update individuals
        for item in self.content:
            # shoot and stuff
            item.update(interval, self.now)
        # create collision maps and sprite composition
        for item in self.content:
            if isinstance(item, entity.Mobile):
                x, y = item.pos
                # prepare sprite list for drawing
                self.add_sprite(x, y, item)
                if isinstance(item, entity.Fragile):
                    # populate collision maps
                    # precompute for faster detection
                    width, height = self.cont.array[item.name].shape
                    identifier = (x, y, x+width, y+height, item)
                    if item.ally:
                        ship_map.append(identifier)
                    else:
                        if isinstance(item, entity.Fighter):
                            self.nb_fighters += 1
                        target_map.append(identifier)
                elif isinstance(item, entity.Catchable):
                    identifier = (x, y, x+item.width, y+item.height, item)
                    bonus_map.append(identifier)
                elif isinstance(item, entity.Projectile):
                        identifier = (x, y, x+item.width, y+item.height, item)
                        if item.ally:
                            ship_proj_map.append(identifier)
                            if isinstance(item, entity.Blast):
                                ship_blast_map.append(identifier)
                        else:
                            target_proj_map.append(identifier)
            elif isinstance(item, entity.Landscape):
                # prepare sprite list for drawing
                self.add_sprite(0, 0, item)
        # update player status
        for player in self.players:
            player.update(interval, self.now)
        # detect collisions and update accordingly
        # catch bonuses, hurray !! \o/
        self.collide(bonus_map, ship_map, self.now)
        # for projectiles against enemies
        self.collide(ship_proj_map, target_map, self.now)
        # between projectiles
        self.collide(target_proj_map, ship_blast_map, self.now)
        # between allies and enemies ships
        self.collide(target_map, ship_map, self.now)
        # enemies can hit us
        self.collide(target_proj_map, ship_map, self.now)
        # evolution of scenery
        if self.nb_fighters < self.level['nb_enemies']:
            fighter = entity.Fighter(self, parameters.SAUCER)
            # add in scene
            fighter.add()
        # update music playback
        self.cont.music()
