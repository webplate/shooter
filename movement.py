#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, math
import entity

def random_up(limits) :
    """a position in upper screen"""
    return (random.randint(0, limits[0]), random.randint(-limits[1]/6, 0))

def pol2cart(radius, angle) :
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y

class Trajectory() :
    """a general position modifier"""
    def __init__(self, scene, mobile) :
        self.scene = scene
        self.mobile = mobile

class Center() :
    """is center of screen"""
    def __init__(self, scene) :
        self.scene = scene
        self.center = self.scene.limits[0]/2, self.scene.limits[0]/2

class AlignV(Trajectory) :
    """align vertically with ship"""
    def __init__(self, scene, mobile) :
        Trajectory.__init__(self, scene, mobile)
        #set init position of mobile
        self.mobile.pos = random_up(self.scene.limits)
        #target healthier player !
        found = False
        max_life = 0
        for item in self.scene.content :
            if isinstance(item, entity.Ship) :
                if item.life > max_life :
                    self.target = item
                    found = True
        if not found :
            #go to center of screen
            self.target = Center(self.scene)

    def new_pos(self, pos, interval) :
        """compute new position from floats"""
        offset =  self.mobile.speed * interval
        #move only if far enough
        distance = abs(self.mobile.center[0] - self.target.center[0])
        if distance > offset :
            if self.target.center[0] > self.mobile.center[0] :
                pos = pos[0] + offset, pos[1]
            elif self.target.center[0] < self.mobile.center[0] :
                pos = pos[0] - offset, pos[1]
        return pos

class AlignH(Trajectory) :
    """align horizontally with ship"""
    def __init__(self, scene, mobile) :
        Trajectory.__init__(self, scene, mobile)
        #set init position of mobile
        self.mobile.pos = random_up(self.scene.limits)

    def new_pos(self, pos, interval) :
        """compute new position from floats"""
        offset =  self.mobile.speed * interval
        #move only if far enough
        distance = abs(self.mobile.center[1] - self.target.center[1])
        if distance > offset :
            if self.target.center[1] > self.mobile.center[1] :
                pos = pos[0] , pos[1] + offset
            elif self.target.center[1] < self.mobile.center[1] :
                pos = pos[0], pos[1] - offset
        return pos

class GoFront(AlignV) :
    """try to be in front of ship"""
    def new_pos(self, pos, interval) :
        pos = AlignV.new_pos(self, pos, interval)
        offset =  self.mobile.speed * interval
        #y coord to reach
        y = self.target.center[1] - self.scene.limits[1]/2
        #move only if far enough
        distance = abs(self.mobile.center[1] - y)
        if distance > offset :
            if y > self.mobile.center[1] :
                pos = pos[0] , pos[1] + offset
            elif y < self.mobile.center[1] :
                #dont go outside screen
                if pos[1] - offset > 0 :
                    pos = pos[0], pos[1] - offset
        return pos

class Circular(GoFront) :
    """orbit around"""
    def __init__(self, scene, mobile) :
        GoFront.__init__(self, scene, mobile)
        #set init position of mobile
        self.ref_pos = random_up(self.scene.limits)
        self.radius = 40
        self.init_angle = random.random() * math.pi * 2
        self.omega = random.random() / 1000 * math.pi * 2
        #one turn each second
        self.angular_speed = 2*math.pi / 1000
        
    def abs_pos(self) :
        #rotate around reference
        angle = self.scene.now * self.angular_speed + self.init_angle
        #oscillating radius
        radius = self.radius * math.sin(self.omega * self.scene.now)
        return pol2cart(radius, angle)

    def rel_pos(self, interval) :
        self.ref_pos = GoFront.new_pos(self, self.ref_pos, interval)
        return self.ref_pos

    def new_pos(self, pos, interval) :
        xrel, yrel = self.rel_pos(interval)
        xabs, yabs = self.abs_pos()
        return xrel+xabs, yrel+yabs
        
