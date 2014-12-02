#!/usr/bin/env python
# -*- coding: utf-8 -*-
import entity, tools, parameters

class Player() :
    """class for player settings, controls, ships"""
    def __init__(self, scene, index) :
        self.scene = scene
        self.index = index
        self.keys = {'up':False, 'down':False, 'right':False, 'left':False,
        'shoot':False}
        self.key_lst = ['right', 'left', 'up', 'down', 'shoot']
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.stop = True
        self.ship = None
        self.latent = self.load_ship(parameters.SHIP)
        self.alive = False
        self.score = 0
        self.life = 0
        self.max_life = 1

    def load_ship(self, parameters) :
        #instantiate according to specified type
        targetClass = getattr(entity, parameters['type'])
        ship = targetClass(self.scene, self, parameters)
        #init position
        coord = (self.scene.limits[0]/2,
        self.scene.limits[1]-self.scene.limits[1]/6)
        ship.pos = coord
        #link to ship attributes
        self.life = ship.life
        self.score = ship.score
        return ship

    def command(self, interval, time) :
        """command ship !!"""
        if self.go_right :
            self.ship.fly('right', interval)
        elif self.go_left :
            self.ship.fly('left', interval)
        if self.go_up :
            self.ship.fly('up', interval)
        elif self.go_down :
            self.ship.fly('down', interval)
        #is the ship charging ?
        if self.keys['shoot'] :
            offset = self.ship.charge_rate * interval
            if self.ship.charge + offset > 1 :
                self.ship.charge = 1.
            else :
                self.ship.charge += offset
        else :
            #charged shot
            if self.ship.charge > 0.5 :
                self.ship.shoot(time, 'Blast', self.ship.charge)
            self.ship.charge = 0.

    def update(self, interval, time) :
        #where is going the ship ?
        if self.keys['right'] and not self.go_right and not self.keys['left'] :
            self.go_right = True
            self.stop = False
        elif not self.keys['right'] and self.go_right :
            self.go_right = False
        if self.keys['left'] and not self.go_left and not self.keys['right'] :
            self.go_left = True
            self.stop = False
        elif not self.keys['left'] and self.go_left :
            self.go_left = False

        if self.keys['up'] and not self.go_up and not self.keys['down'] :
            self.go_up = True
            self.stop = False
        elif not self.keys['up'] and self.go_up :
            self.go_up = False
        if self.keys['down'] and not self.go_down and not self.keys['up'] :
            self.go_down = True
            self.stop = False
        elif not self.keys['down'] and self.go_down :
            self.go_down = False

        if ( not self.keys['up'] and not self.keys['down'] 
        and not self.keys['right'] and not self.keys['left'] ) :
            self.stop = True

        #shoot to join game !!
        if (self.ship == None and self.keys['shoot']) :
            self.alive = True
            self.ship = self.latent
            #summon in scene
            self.ship.add()
        if self.alive :
            self.command(interval, time)
        #update info from ship if it exists
        if self.ship != None :
            self.life = self.ship.life
            self.max_life = self.ship.max_life
            self.score = self.ship.score

class Container():
    """stock surfaces and projectiles maps to prevent duplicates
    stock sounds also
    """
    def __init__(self, scene) :
        self.scene = scene
        self.theme = self.scene.theme['name']
        self.surfaces = {}
        self.array = {}
        self.hit = {}
        self.maps = {}
        self.background = {}
        self.pmap = {}
        self.snds = {}

    def surf(self, name) :
        """avoid duplicate loading"""
        if name in self.surfaces :
            surface = self.surfaces[name]
        else :
            surface = tools.load_image(name, self.theme, self.scene)
            #generate variants of image
            hit = tools.make_white(surface)
            array = tools.make_array(surface)
            self.surfaces.update({name : surface})
            self.hit.update({name : hit})
            self.array.update({name : array})
        return surface

    def proj(self, parameters) :
        if parameters['name'] in self.maps :
            projectile = self.maps[parameters['name']]
        else :
            #instantiate according to specified type
            targetClass = getattr(entity, parameters['type'])
            projectile = targetClass(self.scene, parameters)
            self.maps.update({parameters['name'] : projectile})
        return projectile

    def bg(self, name) :
        """load background images"""
        if name in self.background :
            surface = self.background[name]
        else :
            surface = tools.load_background(name, self.theme, self.scene)
            self.background.update({name : surface})
        return surface

    def snd(self, name) :
        """load sounds"""
        if name in self.snds :
            sound = self.snds[name]
        else :
            sound = tools.load_sound(name, self.scene)
            self.snds.update({name : sound})
        return sound

    def play(self, sound, xpos) :
        p = (self.scene.limits[0] - abs(xpos)) / float(self.scene.limits[0])
        #adjust volume
        p = p * self.scene.snd_pack['effect_volume']
        if not self.scene.mute :
            sound = self.snd(sound)
            if sound != None :
                channel = sound.play()
                channel.set_volume(p, 1-p)

    def load_music(self, track=None, loops=-1):
        if not self.scene.game.no_sound :
            if track != None :
                tools.load_stream(track, self.scene)
                self.scene.game.music.play(loops)
                self.scene.game.music.set_volume(self.scene.snd_pack['music_volume'])

    def music(self) :
        """control game mixer for streaming large music files"""
        if (not self.scene.mute and not self.scene.paused
        and not self.scene.game.no_sound) :
            self.scene.game.music.unpause()
        else :
            self.scene.game.music.pause()

class Ordered():
    """stock objects of scene in layered priority
    """
    def __init__(self) :
        self.content = [[]]

    def __iter__(self) :
        """a generator to emit content in right order"""
        for group in self.content :
            for item in group :
                yield item

    def append(self, item, priority=0) :
        """update size of container dynamically"""
        while len(self.content) <= priority :
            self.content.append([])
        self.content[priority].append(item)

    def remove(self, item) :
        """remove item from content"""
        for group in self.content :
            if item in group :
                group.remove(item)

    def prioritize(self, item, priority) :
        """reorder an item in a specific layer of priority
        or add a new item"""
        #eliminate prior version
        self.remove(item)
        #insert with new priority
        self.append(item, priority)

class Scene() :
    def __init__(self, game) :
        self.game = game
        self.limits = game.limits
        self.font = game.font
        self.mfont = game.mfont
        self.sfont = game.sfont
        self.level = self.game.level
        self.theme = self.level['theme']
        self.snd_pack = self.level['sound_pack']
        self.mute = True
        self.gameplay = self.level['gameplay']
        #an object for efficient loading
        self.cont = Container(self)
        #content in priority update order
        self.content = Ordered()
        self.players = [Player(self, i) for i in range(4)]
        self.player1 = self.players[0]
        self.load_interface()
        #delay between scene and game (scene can be paused)
        self.paused = False
        self.delay = 0
        #launch background music
        self.cont.load_music('background')
        #launch landscape
        entity.Landscape(self, parameters.BACKGROUND).add()
        self.update()

    def load_interface(self) :
        #interface
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
        
        #add in scene
        for item in self.interface :
            item.add()

    def collide_map(self, proj_map, target_map, time) :
        """repercute collisions projectiles and alpha maps of sprites
        dealing with projectile maps (entity.Projectile)"""
        for xP, yP, xPe, yPe, pixel, itemP, index in proj_map :
            #one pixel projectile
            if pixel :
                for xT, yT, xTe, yTe, itemT in target_map :
                    #is in range ?
                    if xP < xTe and xP > xT and yP < yTe and yP > yT :
                        #per pixel collision
                        if self.cont.array[itemT.name][xP - xT, yP - yT] :
                            #hurt or not, entity
                            itemT.collided(itemP, index, time)
                            #remove or not, colliding projectile
                            itemP.collided(index)
            #rectangular projectile
            else :
                for xT, yT, xTe, yTe, itemT in target_map :
                    if xP <= xTe and xPe >= xT and yP <= yTe and yPe >= yT :
                        minx, maxx = max(xP, xT)-xT, min(xPe, xTe)-xT
                        miny, maxy = max(yP, yT)-yT, min(yPe, yTe)-yT
                        if True in self.cont.array[itemT.name][minx:maxx, miny:maxy] :
                            itemT.collided(itemP, index, time)
                            itemP.collided(index)
                            
    def collide_mobile(self, proj_map, target_map, time) :
        """repercute collisions projectiles and alpha maps of sprites
        dealing with projectiles as entities (entity.Mobile)"""
        for xP, yP, xPe, yPe, pixel, itemP in proj_map :
            #one pixel projectile
            if pixel :
                for xT, yT, xTe, yTe, itemT in target_map :
                    #is in range ?
                    if xP < xTe and xP > xT and yP < yTe and yP > yT :
                        #per pixel collision
                        if self.cont.array[itemT.name][xP - xT, yP - yT] :
                            #hurt or not, entity
                            itemT.collided(itemP, None, time)
                            #remove or not, colliding projectile
                            itemP.collided()
            #rectangular projectile
            else :
                for xT, yT, xTe, yTe, itemT in target_map :
                    if xP <= xTe and xPe >= xT and yP <= yTe and yPe >= yT :
                        minx, maxx = max(xP, xT)-xT, min(xPe, xTe)-xT
                        miny, maxy = max(yP, yT)-yT, min(yPe, yTe)-yT
                        if True in self.cont.array[itemT.name][minx:maxx, miny:maxy] :
                            itemT.collided(itemP, index, time)
                            itemP.collided(index)

    def update_paused(self, interval=0, time=0) :
        #stop background music
        self.cont.music()
        #check for resuming
        if not self.paused :
            self.delay += time - self.pause_time
            self.update = self.orig_update

    def pause(self, time) :
        self.pause_time = time
        self.paused = True
        #if paused bypass classic update
        self.orig_update = self.update
        self.update = self.update_paused

    def update(self, interval = 0, time = 0) :
        self.now = time - self.delay
        #collision maps
        ship_map = []
        target_map = []
        ship_proj_map = []
        target_proj_map = []
        bonus_map = []
        #sprite list for drawing
        self.lst_sprites = Ordered()
        self.nb_fighters = 0
        #explore scene
        for item in self.content :
            if isinstance(item, entity.Mobile) :
                x, y = item.pos
                #prepare sprite list for drawing
                identifier = ((x, y), item.surface)
                self.lst_sprites.append(identifier, item.layer)
                if isinstance(item, entity.Fragile) :
                    #populate collision maps
                    #precompute for faster detection
                    width, height = self.cont.array[item.name].shape
                    identifier = (x, y, x+width, y+height, item)
                    if item.ally :
                        ship_map.append(identifier)
                    else :
                        if isinstance(item, entity.Fighter) :
                            self.nb_fighters += 1
                        target_map.append(identifier)
                elif isinstance(item, entity.Catchable) :
                    x, y = item.pos
                    identifier = (x, y, 1, 1, True, item)
                    bonus_map.append(identifier)
            elif isinstance(item, entity.Projectile) :
                for i in range(len(item.positions)) :
                    x, y = item.draw_position(i)
                    identifier = ((x, y), item.surface)
                    self.lst_sprites.append(identifier, item.layer)
                    #blasts have wide damage zone other are on a pixel only
                    if isinstance(item, entity.Blast) :
                        identifier = (x, y, x+item.width, y+item.height, False, item, i)
                    else :
                        x, y = item.position(i)
                        identifier = (x, y, 1, 1, True, item, i)
                    if item.ally :
                        ship_proj_map.append(identifier)
                    else :
                        target_proj_map.append(identifier)
            elif isinstance(item, entity.Landscape) :
                #prepare sprite list for drawing
                identifier = ((0, 0), item.surface)
                self.lst_sprites.append(identifier, item.layer)
        #update player status
        for player in self.players :
            player.update(interval, self.now)
        #detect collisions and update accordingly
        self.collide_map(ship_proj_map, target_map, self.now)
        self.collide_map(target_proj_map, ship_map, self.now)
        #catch bonuses, hurray !! \o/
        self.collide_mobile(bonus_map, ship_map, self.now)
        #evolution of scenery
        if self.nb_fighters < self.level['nb_enemies'] :
            fighter = entity.Fighter(self, parameters.TARGET)
            #add in scene
            fighter.add()
        #update individuals
        for item in self.content :
            #shoot and stuff
            item.update(interval, self.now)
        #update music playback
        self.cont.music()
