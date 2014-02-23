#!/usr/bin/env python
# -*- coding: utf-8 -*-
import entity, surftools, parameters

class Player() :
    """class for player settings, controls, ships"""
    def __init__(self, scene):
        self.scene = scene
        self.keys = {'up':False, 'down':False, 'right':False, 'left':False,
        'shoot':False}
        self.key_lst = ['right', 'left', 'up', 'down', 'shoot']
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.stop = True
        self.ship = None
        self.alive = True
        self.score = 0

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

        if self.ship != None :
            self.command(interval, time)

class Container():
    """stock surfaces and projectiles maps to prevent duplicates
    """
    def __init__(self, scene) :
        self.scene = scene
        self.theme = self.scene.theme['name']
        self.surfaces = {}
        self.array = {}
        self.hit = {}
        self.maps = {}

    def surf(self, name) :
        """avoid duplicate loading"""
        if name in self.surfaces :
            surface = self.surfaces[name]
        else :
            surface = surftools.load_image(name, self.theme, self.scene)
            #generate variants of image
            hit = surftools.make_white(surface)
            array = surftools.make_array(surface)
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
        """reorder an item in a specific layer of priority"""
        #eliminate prior version
        self.remove(item)
        #insert with new priority
        self.append(item, priority)

class Bestiary() :
    """loading and tuning every game objects"""
    def __init__(self, scene) :
        self.scene = scene

    def load_fighter(self, name) :
        fighter = entity.Fighter(self.scene, parameters.TARGET)

    def load_content(self) :
        to_load = self.scene.level['content']
        for parameters in to_load :
            #instantiate according to specified type
            targetClass = getattr(entity, parameters['type'])
            item = targetClass(self.scene, self.scene.player, parameters)
            #init position
            coord = (self.scene.limits[0]/2,
            self.scene.limits[1]-4*self.scene.theme['txt_inter'])
            item.pos = coord

    def load_interface(self) :
        #interface
        score = entity.Widget(self.scene, 'ship.score', ['top', 'left'])
        fps = entity.Widget(self.scene, 'game.fps', ['bottom', 'right', 'low_flip'])
        life = entity.Widget(self.scene, 'ship.life', ['top', 'right'])

class Scene():
    def __init__(self, game) :
        self.game = game
        self.limits = game.limits
        self.font = game.font
        self.level = self.game.level
        self.theme = self.level['theme']
        self.gameplay = self.level['gameplay']
        self.player = Player(self)
        #an object for efficient loading
        self.cont = Container(self)
        #content in priority update order
        self.content = Ordered()
        #layers for drawing
        self.lst_sprites = Ordered()
        self.bestiary = Bestiary(self)
        self.bestiary.load_content()
        for item in self.content :
            if isinstance(item, entity.Ship) :
                self.ship = item
                break
        self.bestiary.load_interface()
        self.update()
        #reference new ship to player
        self.player.ship = self.ship

    def collide(self, proj_map, target_map, time) :
        """repercute collisions projectiles and alpha maps of sprites"""
        for xP, yP, xPe, yPe, pixel, itemP, index in proj_map :
            #one pixel projectile
            if pixel :
                for xT, yT, xTe, yTe, itemT in target_map :
                    #is in range ?
                    if xP < xTe and xP > xT and yP < yTe and yP > yT :
                        #per pixel collision
                        if itemT.array[xP - xT, yP - yT] :
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
                        if True in itemT.array[minx:maxx, miny:maxy] :
                            itemT.collided(itemP, index, time)
                            itemP.collided(index)

    def update(self, interval = 0, time = 0) :
        self.now = time
        #collision maps
        ship_map = []
        target_map = []
        ship_proj_map = []
        target_proj_map = []
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
                    width, height = item.array.shape
                    identifier = (x, y, x+width, y+height, item)
                    if item.ally :
                        ship_map.append(identifier)
                    else :
                        if isinstance(item, entity.Fighter) :
                            self.nb_fighters += 1
                        target_map.append(identifier)
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
        #update player status
        if self.player.alive :
            self.player.update(interval, time)
        #detect collisions and update accordingly
        self.collide(ship_proj_map, target_map, time)
        self.collide(target_proj_map, ship_map, time)
        #evolution of scenery
        if self.nb_fighters < self.level['nb_enemies'] :
            self.bestiary.load_fighter('target')
        #update individuals
        for item in self.content :
            #shoot and stuff
            item.update(interval, time)
