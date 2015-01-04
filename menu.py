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
        self.font_color_inactive = (70, 100, 0)
        self.font = tools.load_font(self.font_name, self.font_size)
        self.bg_color = [50, 50, 50]

        # margins, spacings...
        self.line_spacing = 5
        self.main_menu_margins = [12, 8, 12, 8]

        # container for menu elements
        self.content = []

        # bind menu controls
        self.game.controller.bind_control('up', -1, self)
        self.game.controller.bind_control('down', -1, self)
        self.game.controller.bind_control('enter', -1, self)

        # # # # # # # # #
        # generate menu #
        # # # # # # # # #

        # main menu
        lines = ['Resume', 'New Game', 'Controls', 'Options', 'High Scores', 'Quit']
        self.main_menu = MenuList(self, None, lines, self.line_spacing)
        self.main_menu.visible = True
        self.main_menu.center_lines()
        self.main_menu.center(['x', 'y'])
        self.main_menu.add_border([0,0,0], self.main_menu_margins)
        self.main_menu.add_background(self.bg_color, self.main_menu_margins)
        for line in self.main_menu.lines:
            line.shadow = True
        self.content.append(self.main_menu)

        # options
        lines = ['Back', 'Gameplay', 'Display', 'Sound']
        self.options_menu = MenuList(self, None, lines, self.line_spacing)
        self.options_menu.visible = True
        self.options_menu.center_lines()
        self.options_menu.center(['x', 'y'])
        self.options_menu.add_border([0,0,0], self.main_menu_margins)
        self.options_menu.add_background(self.bg_color, self.main_menu_margins)
        for line in self.options_menu.lines:
            line.shadow = True
        self.content.append(self.options_menu)
        self.options_menu.previous = self.main_menu

        # options/sound
        lines = ['Back', 'Mute']
        self.sound_menu = MenuList(self, None, lines, self.line_spacing)
        self.sound_menu.visible = True
        self.sound_menu.center_lines()
        self.sound_menu.center(['x', 'y'])
        self.sound_menu.add_border([0,0,0], self.main_menu_margins)
        self.sound_menu.add_background(self.bg_color, self.main_menu_margins)
        for line in self.sound_menu.lines:
            line.shadow = True
        self.content.append(self.sound_menu)
        self.sound_menu.previous = self.options_menu

        # active menu at start
        self.active_menu = self.main_menu
        self.active_menu.select_line('first')

    def add_sprites(self, container):
        """add active menu sprites to scene sprite list"""
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
        """trigger function (outside triggers)"""
        if control['name'] == 'open_menu':
            self.active_menu = self.main_menu
            self.active_menu.update()
            self.active_menu.select_line('first')
        else:
            self.active_menu.trigger(control)

    def is_selectable(self, menu_element):
        """function called by elements who want to know if they can be selected"""
        if menu_element.type == 'menu line':
            # generic
            if menu_element.name == 'Back':
                return True
            # main menu
            elif menu_element.name == 'Resume':
                if self.scene.level is not None:
                    return True
            elif menu_element.name == 'New Game':
                return True
            elif menu_element.name == 'Options':
                return True
            elif menu_element.name == 'Quit':
                return True
            # options menu
            elif menu_element.name == 'Sound':
                return True
            elif menu_element.name == 'Mute':
                return True
            else:
                return False

    def action(self, menu_element):
        """function called by selectable elements (inside triggers)"""
        if menu_element.type == 'menu line':
            # generic
            if menu_element.name == 'Back':
                if menu_element.find_previous_menu() is not None:
                    self.active_menu = menu_element.find_previous_menu()
                else:
                    self.active_menu = self.main_menu
                self.active_menu.select_line('first')
            # main menu
            if menu_element.name == 'Resume':
                self.scene.trigger({'name': 'menu'})
            elif menu_element.name == 'New Game':
                self.scene.trigger({'name': 'change_level'})
            elif menu_element.name == 'Options':
                self.options_menu.select_line('first')
                self.active_menu = self.options_menu
            elif menu_element.name == 'Quit':
                self.game.trigger({'name': 'quit'})
            # options menu
            elif menu_element.name == 'Sound':
                self.sound_menu.select_line('first')
                self.active_menu = self.sound_menu
            elif menu_element.name == 'Mute':
                self.scene.trigger({'name': 'mute'})


class MenuElement():
    def __init__(self, menu, parent):
        self.menu = menu
        self.type = 'generic menu element'
        # parent is the menu element which contains the current menu element
        self.parent = parent
        # previous menu is the menu which contains a link to the current menu
        self.previous = None
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
            if item.type not in ['background', 'border']:
                self.size[0] = max(self.size[0], item.rel_pos[0]+item.size[0])
                self.size[1] = max(self.size[1], item.rel_pos[1]+item.size[1])

    def find_previous_menu(self):
        current = self
        while current is not None:
            if current.previous is not None:
                return current.previous
            current = current.parent
        return None

    def add_background(self, color, margins=(0, 0, 0, 0)):
        """
        Add a background to a menu element
        :param margins: extra area around element that should be filled with background color
        """
        background = MenuBackground(self.menu, self, color, margins)
        self.content.append(background)

    def remove_background(self):
        for item in self.content:
            if item.type == 'background':
                self.content.remove(item)

    def add_border(self, color, margins=(0, 0, 0, 0), width=1):
        """
        Add a border to a menu element
        :param margins: extra area around element that should be included inside the border
        """
        border = MenuBorder(self.menu, self, color, margins, width)
        self.content.append(border)

    def remove_border(self):
        for item in self.content:
            if item.type == 'border':
                self.content.remove(item)

    def center(self, axes):
        """
        Center menu element in regard to its parent (or screen if no self.parent = None)
        :param axes: 'x', 'y' or ['x', 'y']
        """
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


class MenuBorder(MenuElement):
    def __init__(self, menu, parent, color, margins, width):
        MenuElement.__init__(self, menu, parent)
        new_margins = list(margins)
        for i, margin in enumerate(margins):
            new_margins[i] = margin+width
        self.type = 'border'
        self.visible = True
        self.layer = parameters.MENUBGLAY
        self.parent.compute_size()
        self.size = parent.size
        self.size[0] += new_margins[0] + new_margins[2]
        self.size[1] += new_margins[1] + new_margins[3]
        self.rel_pos = [-new_margins[0], -new_margins[1]]
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.fill(color)
        rect = [width, width, self.size[0]-1-width, self.size[1]-1-width]
        self.surface.fill([0,0,0,0], rect)


class MenuLine(MenuElement):
    def __init__(self, menu, parent, text):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu line'
        self.text = text
        self.name = text
        self.shadow = False
        self.update()

    def add_shadow(self):
        """generate a pseudo-shadow of the text by adding a background black shifted copy of itself"""
        line_shadow = MenuElement(self.menu, self)
        line_shadow.type = 'shadow'
        line_shadow.surface = self.menu.font.render(self.text, True, [0, 0, 0])
        line_shadow.rel_pos = [1, 1]
        line_shadow.layer = parameters.MENUSHADOWLAY
        line_shadow.visible = True
        self.content.append(line_shadow)

    def get_surface(self):
        if self.selectable:
            return self.menu.font.render(self.text, True, self.menu.font_color)
        else:
            return self.menu.font.render(self.text, True, self.menu.font_color_inactive)

    def update(self):
        self.content = []
        self.surface = self.get_surface()
        if self.shadow:
            self.add_shadow()
        self.selectable = self.menu.is_selectable(self)
        self.compute_size()


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
        elif which == 'first':
            for i, line in enumerate(self.lines):
                if line.selectable:
                    self.selected_line = i
                    break
                else:
                    self.selected_line = None
        if self.selected_line not in range(self.nlines):
            self.selected_line = None

    def update(self):
        for item in self.content:
            item.update()
        for item in self.lines:
            item.remove_background()
            if item.line_number == self.selected_line:
                item.add_background([90, 90, 90], [10, 3, 10, 3])

    def trigger(self, control):
        if control['name'] == 'up' or control['name'] == 'down':
            self.select_line(control['name'])
        if control['name'] == 'enter' and self.selected_line is not None:
            self.menu.action(self.lines[self.selected_line])


class MenuGrid(MenuElement):
    def __init__(self, menu, parent):
        MenuElement.__init__(self, menu, parent)
        self.type = 'menu grid'
