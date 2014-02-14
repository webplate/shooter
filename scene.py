#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Scene():
    def __init__(self, content):
        self.content = content

    def list_sprites(self) :
        for item in self.content :
            yield item.pos, item.surface
            #draw projectile maps
            try :
                projectiles = item.bullets
            except AttributeError :
                projectiles = None
            if projectiles != None :
                for pos in projectiles.positions :
                    yield pos, projectiles.sprite
