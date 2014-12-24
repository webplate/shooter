import pygame.locals as p_l

# 'content' lists all available commands and their associated triggering events
# each line is called a "control" in the program
# each control is structured as
# [ command name, player concerned, event type, event parameters ]
# objects in the program can bind themselves to a control using the Shooter.bind_control method
# (this method can usually be accessed throug scene.game.bind_control)
# Shooter.bind_control_switch is used to bind both 'KEYDOWN' and 'KEYUP' at the same time
# (this method should be used when the program needs the state of the key continuously and not only the event)
# 'main.py' imports this list and handle pygame events by comparing them with bound controls
# if all goes well, this is the only place in the program where the keys used to trigger events will be mentionned

# player concerned:
#   -1              environment
#   0-3             player 1-4

# event types:
#   key pressed     p_l.KEYDOWN
#   key released    p_l.KEYUP
# to be continued

# pygame event types
# http://www.pygame.org/docs/ref/event.html

# pygame keys (for keyboard events)
# http://www.pygame.org/docs/ref/key.html

content_list = [
    # Environment (-1)
    ['quit', -1, p_l.KEYDOWN, p_l.K_ESCAPE],  # Quit game
    ['pause', -1, p_l.KEYDOWN, p_l.K_p],  # Pause game
    ['mute', -1, p_l.KEYDOWN, p_l.K_m],  # Sound on/off
    ['fullscreen', -1, p_l.KEYDOWN, p_l.K_f],  # Fullscreen on/off

    # Player 1 (0)
    # Keyboard control
    ['up', 0, 'SWITCH', p_l.K_UP],
    ['down', 0, 'SWITCH', p_l.K_DOWN],
    ['left', 0, 'SWITCH', p_l.K_LEFT],
    ['right', 0, 'SWITCH', p_l.K_RIGHT],
    ['shoot', 0, 'SWITCH', p_l.K_SPACE],
    # Joystick control
    ['up', 0, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 0, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 0, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 0, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 0, 'JOY_SWITCH', 2],

    # Player 2 (1)
    # Keyboard control
    ['up', 1, 'SWITCH', p_l.K_w],
    ['down', 1, 'SWITCH', p_l.K_s],
    ['left', 1, 'SWITCH', p_l.K_a],
    ['right', 1, 'SWITCH', p_l.K_d],
    ['shoot', 1, 'SWITCH', p_l.K_LSHIFT],
    # Joystick control
    ['up', 1, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 1, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 1, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 1, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 1, 'JOY_SWITCH', 2],

    # Player 3 (2)
    # Joystick control
    ['up', 2, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 2, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 2, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 2, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 2, 'JOY_SWITCH', 2],

    # Player 4 (3)]
    # Joystick control
    ['up', 3, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'negative',  'tol': -0.8}],
    ['down', 3, p_l.JOYAXISMOTION, {'axis': 1, 'direction': 'positive',  'tol': 0.8}],
    ['left', 3, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'negative',  'tol': -0.8}],
    ['right', 3, p_l.JOYAXISMOTION, {'axis': 0, 'direction': 'positive',  'tol': 0.8}],
    ['shoot', 3, 'JOY_SWITCH', 2],
]

key_list = ['name', 'player', 'event_type', 'event_params']
content = []
for control in content_list:
    content_line = {}
    for i, key in enumerate(key_list):
        content_line.update({key_list[i]: control[i]})
    content.append(content_line)
