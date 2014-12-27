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
import scene, parameters, tools, controller, menu


class Shooter():
    """a pygame shooter"""
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
        # display parameters
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
        # load theme from file
        self.theme = parameters.THEME
        self.theme = tools.fill_dict_with_default(self.theme, parameters.DEFAULTTHEME)
        # load fonts
        pygame.font.init()
        self.font = tools.load_font(self.theme['font'],
                                    self.theme['txt_size'])
        self.mfont = tools.load_font(self.theme['monospace_font'],
                                     self.theme['txt_size'])
        self.sfont = tools.load_font(self.theme['small_font'],
                                     self.theme['small_size'])
        # joysticks
        self.joysticks = [[], [], [], [], []]  # josticks linked with each player (1-4 + environment)
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x)
                     for x in range(pygame.joystick.get_count())]
        for joy in joysticks:
            joy.init()
            # append unassigned joystick to environment
            self.joysticks[-1].append(joy.get_id())
            # disable joystick used by Virtual Box (for mouse integration)
            if 'VirtualBox' in joy.get_name():
                joy.quit()
        # time reference
        self.now = 0
        # initialize controller
        self.controller = controller.Controller(self)
        self.controller.toggle_active_controls('global')
        self.controller.toggle_active_controls('menu')
        # initial control binding
        self.controller.bind_control('quit', -1, self)
        self.controller.bind_control('pause', -1, self)
        self.controller.bind_control('mute', -1, self)
        if system != 'Darwin':
            self.controller.bind_control('fullscreen', -1, self)
        # initialize scene
        self.scene = scene.Scene(self)
        # players
        self.players = self.scene.players

    def trigger(self, control):
        if control['name'] == 'quit':
            self.running = False
        elif control['name'] == 'pause':
            if not self.scene.paused:
                self.scene.pause(self.now*self.speed)
            else:
                self.scene.paused = False
        elif control['name'] == 'mute':
            if not self.scene.mute:
                self.scene.mute = True
            else:
                self.scene.mute = False
        elif control['name'] == 'fullscreen':
            if self.fullscreen:
                self.display = pygame.display.set_mode(self.winsize)
            else:
                self.display = pygame.display.set_mode(
                    self.winsize, p_l.HWSURFACE | p_l.FULLSCREEN | p_l.DOUBLEBUF)
                pygame.mouse.set_visible(False)     # hide cursor

    def on_event(self, event):
        """propagate and interpret events"""
        # deal with 'QUIT' event
        if event.type == p_l.QUIT:
            self.trigger(['quit'])

        # deal with other events
        for control in self.controller.active_controls:
            if control['event_type'] == event.type:
                # key pressed
                if event.type == p_l.KEYDOWN:
                    if event.key == control['event_params']['key'] and control['target'] is not None:
                        self.controller.controls_state[control['player']].update({control['name']: True})
                        control['target'].trigger(control)
                # key released
                elif event.type == p_l.KEYUP:
                    if event.key == control['event_params']['key'] and control['target'] is not None:
                        self.controller.controls_state[control['player']].update({control['name']: False})
                        control['target'].trigger(control)
                # gamepad axis motion
                elif control['event_type'] == p_l.JOYAXISMOTION and event.joy in self.joysticks[control['player']]:
                    if event.axis == control['event_params']['axis'] and control['target'] is not None:
                        control['event_params'].update({'joy': event.joy})
                        control['event_params'].update({'value': event.value})
                        control['target'].trigger(control)
                # gamepad button pressed
                elif event.type == p_l.JOYBUTTONDOWN and event.joy in self.joysticks[control['player']]:
                    if event.button == control['event_params']['button'] and control['target'] is not None:
                        self.controller.controls_state[control['player']].update({control['name']: True})
                        control['event_params'].update({'joy': event.joy})
                        control['target'].trigger(control)
                # gamepad button released
                elif event.type == p_l.JOYBUTTONUP and event.joy in self.joysticks[control['player']]:
                    if event.button == control['event_params']['button'] and control['target'] is not None:
                        self.controller.controls_state[control['player']].update({control['name']: False})
                        control['event_params'].update({'joy': event.joy})
                        control['target'].trigger(control)

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
            # EVOLUTION
            self.on_loop()
            # RENDER
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    app = Shooter()
    app.on_execute()

