#!/usr/bin/env python
# -*- coding: utf-8 -*-
import entity

class Scene():
    def __init__(self, content):
        self.content = content

    def list_sprites(self) :
        for item in self.content :
            yield item.pos, item.surface
            #draw projectile maps
            if isinstance(item, entity.Ship) :
                projectiles = item.bullets
                for pos in projectiles.positions :
                    yield pos, projectiles.sprite
