#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def random_up(limits) :
    """a position in upper screen"""
    return (random.randint(0, limits[0]), random.randint(0, limits[1]/6))

class Trajectory() :
    """a general position modifier"""
    def __init__(self, scene, mobile) :
        self.scene = scene
        self.mobile = mobile

class AlignV(Trajectory) :
    """align vertically with ship"""
    def __init__(self, scene, mobile) :
        Trajectory.__init__(self, scene, mobile)
        #set init position of mobile
        self.mobile.pos = random_up(self.scene.limits)

    def new_pos(self, pos, interval) :
        """compute new position from floats"""
        offset =  self.mobile.speed * interval
        #move only if far enough
        distance = abs(self.mobile.center[0] - self.scene.ship.center[0])
        if distance > offset :
            if self.scene.ship.center[0] > self.mobile.center[0] :
                pos = pos[0] + offset, pos[1]
            elif self.scene.ship.pos[0] < self.mobile.center[0] :
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
        distance = abs(self.mobile.center[1] - self.scene.ship.center[1])
        if distance > offset :
            if self.scene.ship.center[1] > self.mobile.center[1] :
                pos = pos[0] , pos[1] + offset
            elif self.scene.ship.pos[1] < self.mobile.center[1] :
                pos = pos[0], pos[1] - offset
        return pos

class GoFront(AlignV) :
    """try to be in front of ship"""
    def new_pos(self, pos, interval) :
        pos = AlignV.new_pos(self, pos, interval)
        offset =  self.mobile.speed * interval
        #y coord to reach
        y = self.scene.ship.center[1] - self.scene.limits[1]/3
        #move only if far enough
        distance = abs(self.mobile.center[1] - y)
        if distance > offset :
            if y > self.mobile.center[1] :
                pos = pos[0] , pos[1] + offset
            elif y < self.mobile.center[1] :
                pos = pos[0], pos[1] - offset
        return pos

