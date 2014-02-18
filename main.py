#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, time, pygame
from parameters import *
import scene

class Shooter():
    """a pygame shooter
    """
    def __init__(self):
        self.running = True
        
    def on_init(self):
        #Set graphic driver according to platform
        system = platform.system()
        if system == 'Windows':    # tested with Windows 7
           os.environ['SDL_VIDEODRIVER'] = 'directx'
        elif system == 'Darwin':   # tested with MacOS 10.5 and 10.6
           os.environ['SDL_VIDEODRIVER'] = 'Quartz'

        #Initialize pygame
        pygame.init()
        self.limits = GAMESIZE
        self.winsize = WINSIZE
        self.display = pygame.display.set_mode(self.winsize)
        self.screen = pygame.Surface(self.limits)
        self.fullscreen = False
        self.fps = 0

        #load fonts
        self.font = pygame.font.Font(txt_font, txt_size) #name, size

        #On compte les joysticks
        nb_joysticks = pygame.joystick.get_count()
        #Et on en crée un s'il y en a au moins un
        if nb_joysticks > 0:
            mon_joystick = pygame.joystick.Joystick(0)
            mon_joystick.init() #Initialisation
        
        #Initialize scene
        self.scene = scene.Scene(self)
        #Players
        self.player = self.scene.player

    def on_event(self, event):
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            self.running = False
        elif event.type == KEYDOWN :
            if event.key == R_key :
                self.player.keys['right'] = True
            elif event.key == L_key :
                self.player.keys['left'] = True
            elif event.key == U_key :
                self.player.keys['up'] = True
            elif event.key == D_key :
                self.player.keys['down'] = True
            elif event.key == Shoot_key :
                self.player.keys['shoot'] = True

            elif event.key == fullscreen_key :
                if self.fullscreen :
                    self.display = pygame.display.set_mode(self.winsize)
                else :
                    self.display = pygame.display.set_mode(self.winsize,
                    HWSURFACE | FULLSCREEN | DOUBLEBUF)
                    pygame.mouse.set_visible(False)     #hide cursor

            
        elif event.type == KEYUP :
            if event.key == R_key :
                self.player.keys['right'] = False
            elif event.key == L_key :
                self.player.keys['left'] = False
            elif event.key == U_key :
                self.player.keys['up'] = False
            elif event.key == D_key :
                self.player.keys['down'] = False
            elif event.key == Shoot_key :
                self.player.keys['shoot'] = False

    def on_loop(self):
        """alter and move objects according to altitude, movement..."""
        new_time = pygame.time.get_ticks()
        interval = new_time - self.last_iter
        self.last_iter = new_time
        #recompute scene status
        self.scene.update(interval, new_time)

    def on_render(self) :
        #compute low res game screen
        self.screen.fill(bg_color)
        for pos, surf in self.scene.lst_sprites :
            self.screen.blit(surf, pos)
        #rescale and display on hd hardware
        pygame.transform.scale2x(self.screen, self.display)
        #flip every 16ms only (for smooth animation, particularly on linux)
        if pygame.time.get_ticks() > self.last_flip + 16 :
            self.fps = 1 / ((pygame.time.get_ticks() - self.last_flip) / 1000.)
            pygame.display.flip()
            self.last_flip = pygame.time.get_ticks()
            self.frame += 1

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False :
            self.running = False
        #Main loop
        self.frame = 0
        self.last_flip = pygame.time.get_ticks()
        self.last_iter = pygame.time.get_ticks()
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
    the_app = Shooter()
    the_app.on_execute()

