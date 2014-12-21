import pygame.locals as p_l

# 'content' lists all available commands and their associated triggering events
# each line is called a "control" in the program
# each control is structured as
# [ command name, player concerned, event type, event parameters ]
# objects in the program can bind themselves to a control using the Shooter.bind_control method
# (this method can usually be accessed throug scene.game.bind_control)
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

content = [
    # Environment (-1)
    ['quit', -1, p_l.KEYDOWN, p_l.K_ESCAPE],  # Quit game
    ['pause', -1, p_l.KEYDOWN, p_l.K_p],  # Pause game
    ['mute', -1, p_l.KEYDOWN, p_l.K_m],  # Sound on/off
    ['fullscreen', -1, p_l.KEYDOWN, p_l.K_f],  # Fullscreen on/off

    # Player 1 (0)
    ['up', 0, p_l.KEYDOWN, p_l.K_UP],
    ['down', 0, p_l.KEYDOWN, p_l.K_DOWN],
    ['left', 0, p_l.KEYDOWN, p_l.K_LEFT],
    ['right', 0, p_l.KEYDOWN, p_l.K_RIGHT],
    ['shoot', 0, p_l.KEYDOWN, p_l.K_SPACE],
    ['shield', 0, p_l.KEYDOWN, p_l.K_v],            # Shield player 0 (test command)


    # Player 2 (1)
    ['up', 1, p_l.KEYDOWN, p_l.K_w],
    ['down', 1, p_l.KEYDOWN, p_l.K_s],
    ['left', 1, p_l.KEYDOWN, p_l.K_a],
    ['right', 1, p_l.KEYDOWN, p_l.K_d],
    ['shoot', 1, p_l.KEYDOWN, p_l.K_LSHIFT],
    ['shield', 1, p_l.KEYDOWN, p_l.K_b],            # Shield player 1 (test command)


    # Player 3 (2)

    # Player 4 (3)]

]