# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l


# # # # # # # # # # # # # #
#   Game Control System   #
# # # # # # # # # # # # # #
#
#   controller.py       Controller class and associated functions
#   controls.py         List of controls
#
# In this file, default controls are defined in a dictionary called 'controls'.
# This dictionary contains several control sets which can be toggled active/inactive by the controller.
# Each control set is a list of 'controls', which are structured as follows:
# [ command name, player concerned, event type, event parameters ]
#
# Once a Controller object is created, objects in the program can bind themselves to a control using
# the Controller.bind_control method (usually accessed through game.controller.bind_control).
# The Controller.bind_control_switch method is used to bind both 'KEYDOWN' and 'KEYUP' at the same time.
# This method should be used when the program needs the state of the key continuously
#
# The Controller object imports 'controls' and deals with control binding and control sets activation
# The main.py 'on_event' function handles events by comparing them with active controls
#
# player concerned:
#   -1              environment
#   0-3             player 1-4
#
# event types:
#   key pressed trigger             p_l.KEYDOWN
#   key released trigger            p_l.KEYUP
#   key pressed (on/off)            'SWITCH'
#   button pressed trigger          p_l.JOYBUTTONDOWN
#   button released trigger         p_l.JOYBUTTONUP
#   button pressed (on/off)         'JOY_SWITCH'
#   joystick axis movement          p_l.JOYAXISMOTION
#   mouse click
#   mouse movement
#
# pygame event types
# http://www.pygame.org/docs/ref/event.html
#
# pygame keys (for keyboard events)
# http://www.pygame.org/docs/ref/key.html
#
# # # # # # # # # # # # # #

# /!\ controls should be unique
controls = {}
# global controls (always active)
controls.update({'global': [
    ['quit', -1, p_l.KEYDOWN, {'key': p_l.K_q}],  # Quit game
    ['mute', -1, p_l.KEYDOWN, {'key': p_l.K_m}],  # Sound on/off
    ['fullscreen', -1, p_l.KEYDOWN, {'key': p_l.K_f}],  # Fullscreen on/off
    ['menu', -1, p_l.KEYDOWN, {'key': p_l.K_ESCAPE}],  # Open menu
]})

# menu controls
controls.update({'menu': [
    ['up', -1, p_l.KEYDOWN, {'key': p_l.K_UP}],
    ['down', -1, p_l.KEYDOWN, {'key': p_l.K_DOWN}],
    ['enter', -1, p_l.KEYDOWN, {'key': p_l.K_RETURN}]
]})

# pause controls
controls.update({'pause': [
    ['pause', -1, p_l.KEYDOWN, {'key': p_l.K_p}],  # Pause / unpause game
]})

# game controls
controls.update({'game': [
    # Environment (-1)
    ['new_player', -1, p_l.JOYBUTTONDOWN, {'button': 2}],

    # Player 1 (0)
    # Keyboard control
    ['up', 0, 'SWITCH', {'key': p_l.K_UP}],
    ['down', 0, 'SWITCH', {'key': p_l.K_DOWN}],
    ['left', 0, 'SWITCH', {'key': p_l.K_LEFT}],
    ['right', 0, 'SWITCH', {'key': p_l.K_RIGHT}],
    ['shoot', 0, 'SWITCH', {'key': p_l.K_SPACE}],
    ['new_player', 0, p_l.KEYDOWN, {'key': p_l.K_SPACE}],
    # Joystick control
    ['up', 0, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 0, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 0, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 0, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 0, 'JOY_SWITCH', {'button': 2}],

    # Player 2 (1)
    # Keyboard control
    ['up', 1, 'SWITCH', {'key': p_l.K_w}],
    ['down', 1, 'SWITCH', {'key': p_l.K_s}],
    ['left', 1, 'SWITCH', {'key': p_l.K_a}],
    ['right', 1, 'SWITCH', {'key': p_l.K_d}],
    ['shoot', 1, 'SWITCH', {'key': p_l.K_LSHIFT}],
    ['new_player', 1, p_l.KEYDOWN, {'key': p_l.K_LSHIFT}],
    # Joystick control
    ['up', 1, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 1, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 1, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 1, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 1, 'JOY_SWITCH', {'button': 2}],

    # Player 3 (2)
    # Joystick control
    ['up', 2, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 2, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 2, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 2, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 2, 'JOY_SWITCH', {'button': 2}],

    # Player 4 (3)]
    # Joystick control
    ['up', 3, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 3, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 3, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 3, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 3, 'JOY_SWITCH', {'button': 2}],
]})