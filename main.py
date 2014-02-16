#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform, os, pygame
from parameters import *
import entity, scene

def load_content(font) :
    ship = entity.Ship((0,window_size[1]-2*txt_inter),
    'ship', font, window_size)
    fighter = entity.Fighter((window_size[0]/2,0),
    'target', font, window_size)
    fighter2 = entity.Fighter((window_size[0]/3,200),
    'target', font, window_size)
    content = [ship, fighter, fighter2]
    return content

class Player() :
    def __init__(self):
        self.keys = {'up':False, 'down':False, 'right':False, 'left':False,
        'shoot':False}
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False

    def update(self) :
        #where is going the ship ?
        if self.keys['right'] and not self.go_right and not self.keys['left'] :
            self.go_right = True
        elif not self.keys['right'] and self.go_right :
            self.go_right = False
        if self.keys['left'] and not self.go_left and not self.keys['right'] :
            self.go_left = True
        elif not self.keys['left'] and self.go_left :
            self.go_left = False

        if self.keys['up'] and not self.go_up and not self.keys['down'] :
            self.go_up = True
        elif not self.keys['up'] and self.go_up :
            self.go_up = False
        if self.keys['down'] and not self.go_down and not self.keys['up'] :
            self.go_down = True
        elif not self.keys['down'] and self.go_down :
            self.go_down = False

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
        content = load_content(self.font)
        self.scene = scene.Scene(content)
        for item in self.scene.content :
            if isinstance(item, entity.Ship) :
                self.ship = item
                break


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
                self.ship.shoot()
            
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
        '''alter and move objects according to altitude, movement...'''
        interval = pygame.time.get_ticks() - self.last_iter
        self.player.update()
        if self.player.go_right :
            self.ship.move('right', interval)
        elif self.player.go_left :
            self.ship.move('left', interval)
        if self.player.go_up :
            self.ship.move('up', interval)
        elif self.player.go_down :
            self.ship.move('down', interval)

        self.scene.update(interval)
        self.last_iter = pygame.time.get_ticks()

    def on_render(self) :
        self.display.fill(bg_color)
        sprites = self.scene.list_sprites()
        for pos, surf in sprites :
            self.display.blit(surf, pos)
        #flip every 16ms only (for smooth animation, particularly on linux)
        if pygame.time.get_ticks() > self.last_flip + 8 :
            fps = 1 / ((pygame.time.get_ticks() - self.last_flip) / 1000.)
            fps = str(int(fps))
            surf = self.font.render(fps, False, txt_color)
            self.display.blit(surf, (0,0))
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
            #evt = pygame.event.wait()
            evts = pygame.event.get()
            #evts.insert(0, evt)
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

