#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

class Trajectory() :
    """a general position modifier"""
    def __init__(self, scene, mobile) :
        self.scene = scene
        self.mobile = mobile

class Align(Trajectory) :
    """align vertically with ship"""
    def __init__(self, scene, mobile) :
        Trajectory.__init__(self, scene, mobile)
        #set init position of mobile
        self.mobile.pos = (random.randint(0, self.scene.limits[0]),
        random.randint(0, self.scene.limits[1]/6))

    def new_pos(self, pos, interval) :
        offset =  self.mobile.speed * interval
        #move only if far enough
        distance = abs(self.mobile.center[0] - self.scene.ship.center[0])
        if distance > offset :
            if self.scene.ship.center[0] > self.mobile.center[0] :
                pos = pos[0] + offset, pos[1]
            elif self.scene.ship.pos[0] < self.mobile.center[0] :
                pos = pos[0] - offset, pos[1]
        return pos
