#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
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
#  
import platform, os, pygame
import pygame.locals as p_l
import scene, parameters

def load_level(level) :
    """make sure the loaded level is playable"""
    ref = parameters.DEFAULTLEVEL
    for key in ref :
        if key not in level :
            level.update({key : ref[key]})
    return level

class Shooter() :
    """a pygame shooter
    """
    def __init__(self) :
        """initialize game"""
        self.running = True
        #Set graphic driver according to platform
        system = platform.system()
        if system == 'Windows':    # tested with Windows 7
            os.environ['SDL_VIDEODRIVER'] = 'directx'
        elif system == 'Darwin':   # tested with MacOS 10.5 and 10.6
            os.environ['SDL_VIDEODRIVER'] = 'Quartz'
        #Initialize pygame
        pygame.init()
        self.limits = parameters.GAMESIZE
        self.scale = parameters.RESCALE
        if self.scale in ['mame', '2x'] :
            self.winsize = self.limits[0]*2, self.limits[1]*2
        else :
            self.winsize = self.limits
        self.display = pygame.display.set_mode(self.winsize)
        self.screen = pygame.Surface(self.limits)
        self.fullscreen = False
        self.fps = 0
        #load content from file
        self.level = load_level(parameters.LEVEL)
        self.theme = self.level['theme']
        #load fonts
        self.font = pygame.font.Font(self.theme['font'], self.theme['txt_size'])
        #joysticks
        joysticks = [pygame.joystick.Joystick(x)
        for x in range(pygame.joystick.get_count())]
        for joy in joysticks :
            joy.init()
        #Initialize scene
        self.scene = scene.Scene(self)
        #Players
        self.players = self.scene.players

    def on_event(self, event) :
        """propagate and interpret events"""
        if (event.type == p_l.QUIT or
        (event.type == p_l.KEYDOWN and event.key == p_l.K_ESCAPE)) :
            self.running = False
        elif event.type == p_l.KEYDOWN :
            for i, keymap in enumerate(parameters.KEYMAPS) :
                if event.key in keymap :
                    #update player key status
                    key = keymap[event.key]
                    if key in self.players[i].keys :
                        self.players[i].keys[key] = True
                    #switch to fullscreen
                    if key == 'fullscreen' :
                        if self.fullscreen :
                            self.display = pygame.display.set_mode(self.winsize)
                        else :
                            self.display = pygame.display.set_mode(self.winsize,
                            p_l.HWSURFACE | p_l.FULLSCREEN | p_l.DOUBLEBUF)
                            pygame.mouse.set_visible(False)     #hide cursor

                    elif key == 'pause' :
                        if self.scene.running :
                            self.scene.pause(pygame.time.get_ticks())
                        else :
                            self.scene.unpause(pygame.time.get_ticks())
                            

                        
        elif event.type == p_l.KEYUP :
            for i, keymap in enumerate(parameters.KEYMAPS) :
                if event.key in keymap :
                    #update player key status
                    key = keymap[event.key]
                    if key in self.players[i].keys :
                        self.players[i].keys[key] = False
        #Joystick events
        elif event.type == p_l.JOYAXISMOTION :
            tol = 0.8
            if event.axis == 0 :
                if event.value < tol and event.value > -tol :
                    self.players[event.joy].keys['right'] = False
                    self.players[event.joy].keys['left'] = False
                elif event.value < tol :
                    self.players[event.joy].keys['right'] = False
                    self.players[event.joy].keys['left'] = True
                elif event.value > -tol :
                    self.players[event.joy].keys['right'] = True
                    self.players[event.joy].keys['left'] = False
            elif event.axis == 1 :
                if event.value < tol and event.value > -tol :
                    self.players[event.joy].keys['up'] = False
                    self.players[event.joy].keys['down'] = False
                elif event.value < tol :
                    self.players[event.joy].keys['up'] = True
                    self.players[event.joy].keys['down'] = False
                elif event.value > -tol :
                    self.players[event.joy].keys['up'] = False
                    self.players[event.joy].keys['down'] = True
        elif event.type == p_l.JOYBUTTONDOWN :
            if event.button == 2 :
                self.players[event.joy].keys['shoot'] = True
        elif event.type == p_l.JOYBUTTONUP :
            if event.button == 2 :
                self.players[event.joy].keys['shoot'] = False

    def on_loop(self) :
        """alter and move objects according to altitude, movement..."""
        new_time = pygame.time.get_ticks()
        interval = new_time - self.last_iter
        self.last_iter = new_time
        #recompute scene status
        self.scene.update(interval, new_time)

    def on_render(self) :
        """create screen frames"""
        #compute low res game screen
        self.screen.fill(self.theme['bg_color'])
        for pos, surf in self.scene.lst_sprites :
            self.screen.blit(surf, pos)
        #rescale for display on hd hardware
        if self.scale == 'mame' :
            pygame.transform.scale2x(self.screen, self.display)
        elif self.scale == '2x' :
            pygame.transform.scale(self.screen, self.winsize, self.display)
        else :
            self.display.blit(self.screen, (0, 0))
        #limit flipping rate
        if pygame.time.get_ticks() > self.last_flip + 8 :
            self.fps = 1 / ((pygame.time.get_ticks() - self.last_flip) / 1000.)
            pygame.display.flip()
            self.last_flip = pygame.time.get_ticks()
            self.frame += 1

    def on_cleanup(self) :
        pygame.quit()

    def on_execute(self) :
        """launch mainloop"""
        #Main loop
        self.frame = 0
        now = pygame.time.get_ticks()
        self.last_flip = now
        self.last_iter = now
        while self.running:
            #EVENTS
            evts = pygame.event.get()
            for event in evts:
                self.on_event(event)
            #EVOLUTION
            self.on_loop()
            #RENDER
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    app = Shooter()
    app.on_execute()

