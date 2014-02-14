#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Scene():
    def __init__(self, content):
        self.content = content


    def list_sprites(self) :
        for item in self.content :
            yield item.pos, item.surface
