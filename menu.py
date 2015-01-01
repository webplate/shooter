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
        self.line_spacing = 5
        self.main_menu_margins = [12, 8, 12, 8]

        # container for menu elements
        self.content = []

        # bind menu controls
        self.game.controller.bind_control('up', -1, self)
        self.game.controller.bind_control('down', -1, self)
        self.game.controller.bind_control('enter', -1, self)

        # describe menus
        lines = ['Resume', 'New Game', 'Controls', 'High Scores', 'Quit']
        main_menu = MenuList(self, None, lines, self.line_spacing)
        main_menu.visible = True
        main_menu.center_lines()
        main_menu.center(['x', 'y'])
        main_menu.add_background(self.bg_color, self.main_menu_margins)
        self.content.append(main_menu)
        self.active_menu = main_menu

    def add_sprites(self, container):
        for item in container.content:
            if item.visible and item.surface is not None:
                self.scene.add_sprite(item.abs_pos[0], item.abs_pos[1], item)
        for item in container.content:
            if item.visible:
                self.add_sprites(item)

    def update(self):
        for item in self.content:
            item.update()

    def trigger(self, control):
        self.active_menu.trigger(control)


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
        # container for other menu elements
        self.content = []

    def update(self):
        for item in self.content:
            item.update()

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
            if item.type is not 'background':
                self.size[0] = max(self.size[0], item.rel_pos[0]+item.size[0])
                self.size[1] = max(self.size[1], item.rel_pos[1]+item.size[1])

    def add_background(self, color, margins=[0, 0, 0, 0]):
        background = MenuBackground(self.menu, self, color, margins)
        self.content.append(background)

    def remove_background(self):
        for item in self.content:
            if item.type == 'background':
                self.content.remove(item)

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
    def __init__(self, menu, parent, color, margins):
        MenuElement.__init__(self, menu, parent)
        self.type = 'background'
        self.visible = True
        self.layer = parameters.MENUBGLAY
        self.parent.compute_size()
        self.size = parent.size
        self.size[0] += margins[0] + margins[2]
        self.size[1] += margins[1] + margins[3]
        self.rel_pos = [-margins[0], -margins[1]]
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
        self.lines = []
        self.nlines = 0
        self.selected_line = None

        for i, txt in enumerate(texts):
            line = MenuLine(self.menu, self, txt)
            line.visible = True
            line.selectable = True
            line.line_number = i
            # notice the little trick to avoid line spacing before first line
            line.rel_pos = [0, self.size[1] + min(i, 1)*self.line_spacing]
            self.lines.append(line)
            self.content.append(line)
            self.nlines += 1
            self.compute_size()

    def center_lines(self):
        """center all lines of the list"""
        for item in self.content:
            if item.type == 'menu line':
                item.center('x')

    def select_line(self, which):
        """select next or previous selectable line"""
        if which == 'down':
            if self.selected_line is None:
                self.selected_line = -1
            for i in range(self.nlines):
                if self.lines[(i+1+self.selected_line) % self.nlines].selectable:
                    self.selected_line = (i+1+self.selected_line) % self.nlines
                    break
        elif which == 'up':
            if self.selected_line is None:
                self.selected_line = self.nlines
            for i in range(self.nlines).__reversed__():
                if self.lines[(i+self.selected_line) % self.nlines].selectable:
                    self.selected_line = (i+self.selected_line) % self.nlines
                    break
        if self.selected_line not in range(self.nlines):
            self.selected_line = None

    def update(self):
        for item in self.content:
            if item.type == 'menu line':
                if item.line_number == self.selected_line:
                    item.add_background([90, 90, 90], [10, 3, 10, 3])
                else:
                    item.remove_background()
            item.update()

    def trigger(self, control):
        if control['name'] == 'up' or control['name'] == 'down':
            self.select_line(control['name'])


class MenuGrid(MenuElement):
    def __init__(self, menu, parent):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu grid'
