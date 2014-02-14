#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, threading, pygame, operator
from parameters import *
import objects, scene

class Player() :
    def __init__(self):
        self.go_right = False
        self.go_left = False

class Shooter():
    '''a pygame shooter
    '''
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
        if full_screen:
            self.display = pygame.display.set_mode(window_size,
            HWSURFACE | FULLSCREEN | DOUBLEBUF)
            pygame.mouse.set_visible(False)     #hide cursor
        else:
            self.display = pygame.display.set_mode(window_size)

        #load fonts
        self.font = pygame.font.Font(txt_font, txt_size) #name, size

        #On compte les joysticks
        nb_joysticks = pygame.joystick.get_count()
        #Et on en crée un s'il y en a au moins un
        if nb_joysticks > 0:
            mon_joystick = pygame.joystick.Joystick(0)
            mon_joystick.init() #Initialisation
        #Players
        self.player = Player()
        #Initialize scene
        self.ship = objects.Ship((0,window_size[1]-2*txt_inter),
        'ship', self.font)
        content = [self.ship, objects.Mobile_sprite((0,0), 'target', self.font)]
        self.scene = scene.Scene(content)


    def on_event(self, event):
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            self.running = False
        elif event.type == KEYDOWN :
            if event.key == R_key and not self.player.go_left:
                self.player.go_right = True
            elif event.key == L_key and not self.player.go_right:
                self.player.go_left = True
        elif event.type == KEYUP :
            if event.key == R_key :
                self.player.go_right = False
            elif event.key == L_key :
                self.player.go_left = False

    def on_loop(self):
        '''alter and move objects according to altitude, movement...'''
        interval = pygame.time.get_ticks() - self.last_flip
        if self.player.go_right :
            self.ship.move('right', interval)
        elif self.player.go_left :
            self.ship.move('left', interval)
        
    def on_render(self) :
        self.display.fill(bg_color)
        sprites = self.scene.list_sprites()
        for pos, surf in sprites :
            self.display.blit(surf, pos)
        #flip every 16ms only (for smooth animation, particularly on linux)
        if pygame.time.get_ticks() > self.last_flip + 16 :
            self.last_flip = pygame.time.get_ticks()
            pygame.display.flip()
            self.frame += 1

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False :
            self.running = False
        #Main loop
        self.frame = 0
        self.last_flip = pygame.time.get_ticks()
        while self.running:
            #EVENTS
            evt = pygame.event.wait()
            evts = pygame.event.get()
            evts.insert(0, evt)
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

