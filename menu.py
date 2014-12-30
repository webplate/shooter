# !/usr/bin/env python
# -*- coding: utf-8 -*-
import tools
import parameters
import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.scene = game.scene

        self.font_name = "FIXED_BO.TTF"
        self.font_size = 9
        self.font_color = (140, 200, 0)
        self.font = tools.load_font(self.font_name, self.font_size)
        self.bg_color = [40, 40, 40]
        self.x_margin = 10
        self.y_margin = 5

        self.content = []
        self.size = [0, 0]
        self.pos = [float('inf'), float('inf')]

        # line = MenuLine(self, 'Test menu line')
        # line.visible = True
        # self.content.append(line)

        menulist = MenuList(self, ['Resume', 'New Game', 'Controls', 'High Scores', 'Quit'])
        menulist.visible = True
        self.content.append(menulist)

        self.make_background()

    def add_sprites(self, container):
        for item in container.content:
            if hasattr(item, 'content') and item.visible:
                self.add_sprites(item)
            else:
                self.scene.add_sprite(item.pos[0], item.pos[1], item)

    def make_background(self):
        for item in self.content:
            self.pos[0] = min(self.pos[0], item.pos[0])
            self.pos[1] = min(self.pos[1], item.pos[1])
            self.size[0] = max(self.size[0], item.size[0])
            self.size[1] = max(self.size[1], item.size[1])
        self.pos = self.pos[0]-self.x_margin, self.pos[1]-self.y_margin
        self.size = self.size[0]+2*self.x_margin, self.size[1]+2*self.y_margin
        background = MenuElement(self)
        background.visible = True
        background.layer = parameters.MENUBGLAY
        background.pos = self.pos
        background.size = self.size
        background.surface = pygame.Surface(self.size)
        background.surface.fill(self.bg_color)
        self.content.append(background)




class MenuElement():
    def __init__(self, menu):
        self.menu = menu
        self.visible = False
        self.selectable = False
        self.layer = parameters.MENULAY
        self.surface = None
        self.pos = [0, 0]
        self.size = [0, 0]

    def x_center(self):
        if hasattr(self, 'size'):
            self.pos[0] = parameters.GAMESIZE[0] / 2 - self.size[0] / 2
        elif self.surface is not None:
            self.pos[0] = parameters.GAMESIZE[0] / 2 - self.surface.get_width() / 2

    def y_center(self):
        if hasattr(self, 'size'):
            self.pos[1] = parameters.GAMESIZE[1] / 2 - self.size[1] / 2
        elif self.surface is not None:
            self.pos[1] = parameters.GAMESIZE[1] / 2 - self.surface.get_height() / 2


class MenuLine(MenuElement):
    def __init__(self, menu, text):
        MenuElement.__init__(self, menu)
        self.text = text
        self.size = menu.font.size(self.text)
        self.selected_color = [100, 100, 100]
        self.selected = False

        self.surface = self.get_surface()

    def get_surface(self):
        if self.selected:
            surface = self.menu.font.render(self.text, True, self.menu.font_color, self.selected_color)
        else:
            surface = self.menu.font.render(self.text, True, self.menu.font_color)
        return surface


class MenuList(MenuElement):
    def __init__(self, menu, texts):
        MenuElement.__init__(self, menu)
        self.content = []
        self.line_spacing = 5

        for txt in texts:
            line = MenuLine(menu, txt)
            line.visible = True
            line.pos = [self.pos[0], self.pos[1]+self.size[1]]
            line.x_center()
            self.size[0] = max(self.size[0], line.size[0])
            self.size[1] += menu.font.size(line.text)[1] + self.line_spacing
            self.content.append(line)
        self.size[1] -= self.line_spacing

        self.x_center()
        self.y_center()

        for line in self.content:
            line.pos[1] += self.pos[1]


class MenuGrid(MenuElement):
    def __init__(self, menu):
        pass