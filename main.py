# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import platform, os, pygame
import pygame.locals as p_l
import scene, parameters, tools, controls


def load_level(level):

    """make sure the loaded level is playable"""
    ref = parameters.DEFAULTLEVEL
    for key in ref:
        if key not in level:
            level.update({key: ref[key]})
        elif key in ['theme', 'gameplay', 'sound_pack']:
            ref2 = ref[key]
            for key2 in ref2:
                if key2 not in level[key]:
                    level[key].update({key2: ref2[key2]})
    return level


class Shooter():
    """a pygame shooter
    """
    def __init__(self):
        """initialize game"""
        self.running = True
        # Set graphic driver according to platform
        system = platform.system()
        if system == 'Windows':    # tested with Windows 7
            os.environ['SDL_VIDEODRIVER'] = 'directx'
        elif system == 'Darwin':   # tested with MacOS 10.5 and 10.6
            os.environ['SDL_VIDEODRIVER'] = 'Quartz'
        # Initialize pygame
        # only necessary modules
        # try to init sound mixer
        try:
            # small buffer for low latency sound (speedy gameplay)
            pygame.mixer.init(buffer=64)
        # support systems with no sound card
        except pygame.error:
            self.no_sound = True
        else:
            # large number of channels for many sounds
            pygame.mixer.set_num_channels(256)
            # a music mixer for background music
            self.music = pygame.mixer.music
            self.no_sound = False
        # an object to keep track of time
        # necessary to launch pygame passing time
        self.clock = pygame.time.Clock()
        self.interval = 0
        self.speed = parameters.DEFAULTPLAY['game_speed']
        self.flip_rate = parameters.DEFAULTPLAY['flip_rate']
        self.frame_limit = 1000. / self.flip_rate   # max time for a scene update
        self.limits = parameters.GAMESIZE
        self.scale = parameters.RESCALE
        if self.scale in ['mame', '2x']:
            self.winsize = self.limits[0]*2, self.limits[1]*2
        else:
            self.winsize = self.limits
        self.display = pygame.display.set_mode(self.winsize)
        self.screen = pygame.Surface(self.limits)
        self.fullscreen = False
        self.fps = 0
        # load content from file
        self.level = load_level(parameters.LEVEL)
        self.theme = self.level['theme']
        # load fonts
        pygame.font.init()
        self.font = tools.load_font(self.theme['font'],
                                    self.theme['txt_size'])
        self.mfont = tools.load_font(self.theme['monospace_font'],
                                     self.theme['txt_size'])
        self.sfont = tools.load_font(self.theme['small_font'],
                                     self.theme['small_size'])
        # joysticks
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        for joy in joysticks:
            joy.init()
            # disable joystick used by Virtual Box (for mouse integration)
            if 'VirtualBox' in joy.get_name():
                joy.quit()
        # time reference
        self.now = 0
        # Load Controls
        # self.controls = [
        #     ['Missile', 0, p_l.KEYDOWN, 118],
        #     ['Shield', 0, p_l.KEYUP, 118]
        # ]
        self.controls = controls.content
        self.bound_controls = []
        # Initialize scene
        self.scene = scene.Scene(self)
        # Players
        self.players = self.scene.players

    def bind_control(self, control_name, player, target):
        """bind a control event to a target
        target.trigger will be called using adequate arguments
        """
        for control in self.controls:
            if control[0] == control_name and control[1] == player:
                control.append(target)
                self.bound_controls.append(control)
                print control, '( player', player, ') bound to', target

    def on_event(self, event):
        """propagate and interpret events"""

        for control in self.bound_controls:
            if control[2] == event.type:
                # key pressed
                if event.type == p_l.KEYDOWN:
                    if event.key == control[3]:
                        if control[4] is not None:
                            control[4].trigger(control)
                # key released
                elif control[2] == p_l.KEYUP:
                    if event.key == control[3]:
                        if control[4] is not None:
                            control[4].trigger(control)

        if (event.type == p_l.QUIT or
        (event.type == p_l.KEYDOWN and event.key == p_l.K_ESCAPE)):
            self.running = False
        elif event.type == p_l.KEYDOWN:
            for i, keymap in enumerate(parameters.KEYMAPS):
                if event.key in keymap:
                    # update player key status
                    key = keymap[event.key]
                    if key in self.players[i].keys:
                        self.players[i].keys[key] = True
                    # switch to fullscreen
                    if key == 'fullscreen':
                        if self.fullscreen:
                            self.display = pygame.display.set_mode(self.winsize)
                        else:
                            self.display = pygame.display.set_mode(self.winsize,
                            p_l.HWSURFACE | p_l.FULLSCREEN | p_l.DOUBLEBUF)
                            pygame.mouse.set_visible(False)     # hide cursor
                    elif key == 'pause':
                        if not self.scene.paused:
                            self.scene.pause(self.now*self.speed)
                        else:
                            self.scene.paused = False
                    elif key == 'mute':
                        if not self.scene.mute:
                            self.scene.mute = True
                        else:
                            self.scene.mute = False
        elif event.type == p_l.KEYUP:
            for i, keymap in enumerate(parameters.KEYMAPS):
                if event.key in keymap:
                    # update player key status
                    key = keymap[event.key]
                    if key in self.players[i].keys:
                        self.players[i].keys[key] = False

        # Joystick events
        elif event.type == p_l.JOYAXISMOTION:
            tol = 0.8
            if event.axis == 0:
                if abs(event.value) < tol:
                    self.players[event.joy].keys['right'] = False
                    self.players[event.joy].keys['left'] = False
                elif event.value < tol:
                    self.players[event.joy].keys['right'] = False
                    self.players[event.joy].keys['left'] = True
                elif event.value > -tol:
                    self.players[event.joy].keys['right'] = True
                    self.players[event.joy].keys['left'] = False
            elif event.axis == 1:
                if abs(event.value) < tol:
                    self.players[event.joy].keys['up'] = False
                    self.players[event.joy].keys['down'] = False
                elif event.value < tol:
                    self.players[event.joy].keys['up'] = True
                    self.players[event.joy].keys['down'] = False
                elif event.value > -tol:
                    self.players[event.joy].keys['up'] = False
                    self.players[event.joy].keys['down'] = True
        elif event.type == p_l.JOYBUTTONDOWN:
            if event.button == 2:
                self.players[event.joy].keys['shoot'] = True
        elif event.type == p_l.JOYBUTTONUP:
            if event.button == 2:
                self.players[event.joy].keys['shoot'] = False

    def on_loop(self):
        """alter and move objects according to altitude, movement..."""
        if self.interval > self.frame_limit:
            self.interval = self.frame_limit
        self.now += self.interval
        # recompute scene status
        self.scene.update(self.interval*self.speed, self.now*self.speed)

    def on_render(self):
        """create screen frames"""
        # compute low res game screen
        self.screen.fill(self.theme['bg_color'])
        for pos, surf in self.scene.lst_sprites:
            self.screen.blit(surf, pos)
        # rescale for display on hd hardware
        if self.scale == 'mame':
            pygame.transform.scale2x(self.screen, self.display)
        elif self.scale == '2x':
            pygame.transform.scale(self.screen, self.winsize, self.display)
        else:
            self.display.blit(self.screen, (0, 0))
        # limit flipping rate
        self.interval = self.clock.tick_busy_loop(self.flip_rate)
        self.fps = self.clock.get_fps()
        pygame.display.flip()
        self.frame += 1

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        """launch mainloop"""
        # Main loop
        self.frame = 0
        while self.running:
            # EVENTS
            evts = pygame.event.get()
            for event in evts:
                self.on_event(event)
                print event
            # EVOLUTION
            self.on_loop()
            # RENDER
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    app = Shooter()
    app.on_execute()

