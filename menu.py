# !/usr/bin/env python
# -*- coding: utf-8 -*-
import tools
import parameters
import pygame


# all menu elements have a relative position (rel_pos)
# this position indicates where they should be placed relatively to their parent


class Menu():
    """handler for all menu elements"""
    def __init__(self, game):
        # addresses of game and scene
        self.game = game
        self.scene = game.scene

        # fonts and colors
        self.font_name = "FIXED_BO.TTF"
        self.font_size = 9
        self.font_color = (140, 200, 0)
        self.font_color_inactive = (100, 150, 0)
        self.font = tools.load_font(self.font_name, self.font_size)
        self.bg_color = [40, 40, 40]

        # margins, spacings...
        self.x_margin = 10
        self.y_margin = 5

        # container for menu elements
        self.content = []

        main_menu = MenuList(self, None, ['Resume', 'New Game', 'Controls', 'High Scores', 'Quit'], 5)
        main_menu.visible = True
        main_menu.center_lines()
        main_menu.center(['x', 'y'])

        self.content.append(main_menu)

        main_menu.add_background([0, 0, 0])

    def add_sprites(self, container):
        for item in container.content:
            if item.visible and item.surface is not None:
                self.scene.add_sprite(item.abs_pos[0], item.abs_pos[1], item)
        for item in container.content:
            if item.visible:
                self.add_sprites(item)

    def update(self):
        for item in self.content:
            item.update


class MenuElement():
    def __init__(self, menu, parent):
        self.menu = menu
        self.type = 'generic menu element'
        self.parent = parent
        self.visible = False
        self.selectable = False
        self.surface = None
        self.layer = parameters.MENULAY
        self.rel_pos = [0, 0]
        self.size = [0, 0]
        # left, top, right, bottom
        self.margins = [0, 0, 0, 0]
        # container for other menu elements
        self.content = []

    def update(self):
        for item in self.content:
            item.update()
        self.compute_size()

    # absolute position is obtained by recursively adding all relative positions of parents
    def get_abs_pos(self):
        abs_pos = list(self.rel_pos)
        current = self
        while current.parent is not None:
            abs_pos[0] += current.parent.rel_pos[0]
            abs_pos[1] += current.parent.rel_pos[1]
            current = current.parent
        return abs_pos
    abs_pos = property(get_abs_pos)

    def compute_size(self):
        # size due to own surface
        if self.surface is not None:
            self.size[0] = self.surface.get_width()
            self.size[1] = self.surface.get_height()
        else:
            self.size = [0, 0]
        # size due to content
        for item in self.content:
            self.size[0] = max(self.size[0], item.rel_pos[0]+item.size[0])
            self.size[1] = max(self.size[1], item.rel_pos[1]+item.size[1])

    def add_background(self, color):
        background = MenuBackground(self.menu, self, color)
        self.content.append(background)

    def center(self, axes):
        for axis in axes:
            if axis == 'x':
                axis = 0
            elif axis == 'y':
                axis = 1
            self.compute_size()
            # item has a parent (another menu element)
            if self.parent is not None:
                self.parent.compute_size()
                self.rel_pos[axis] = self.parent.size[axis]/2 - self.size[axis]/2
            # item has no parent: center on screen
            else:
                self.rel_pos[axis] = parameters.GAMESIZE[axis]/2 - self.size[axis]/2


class MenuBackground(MenuElement):
    def __init__(self, menu, parent, color):
        MenuElement.__init__(self, menu, parent)
        self.type = 'background'
        self.visible = True
        self.layer = parameters.MENUBGLAY
        self.size = parent.size
        self.surface = pygame.Surface(self.size)
        self.surface.fill(color)


class MenuLine(MenuElement):
    def __init__(self, menu, parent, text):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu line'
        self.text = text
        self.surface = self.get_surface()
        self.compute_size()

    def get_surface(self):
        surface = self.menu.font.render(self.text, True, self.menu.font_color)
        return surface


class MenuList(MenuElement):
    def __init__(self, menu, parent, texts, line_spacing=0):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu list'
        self.line_spacing = line_spacing

        for i, txt in enumerate(texts):
            line = MenuLine(self.menu, self, txt)
            line.visible = True
            line.number = i
            # notice the little trick to get line spacings only between lines
            line.rel_pos = [0, self.size[1] + min(i, 1)*self.line_spacing]
            self.content.append(line)
            self.compute_size()

        # self.content[0].add_background([255, 0, 0])

    def center_lines(self):
        for item in self.content:
            if item.type == 'menu line':
                item.center('x')


class MenuGrid(MenuElement):
    def __init__(self, menu, parent):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu grid'
