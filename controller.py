# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l
import controls


class Controller():
    """a handler for game controls"""
    def __init__(self, game):
        self.game = game
        # load static controls from controls.py
        self.controls = controls.content
        # create empty lists of bound controls (those who are used)
        self.bound_controls = {}
        self.active_controls_set = {}
        for key in self.controls:
            self.bound_controls.update({key: []})
            self.active_controls_set.update({key: False})
        self.active_controls = []
        # create a list of dictionaries containing control switches for each player
        # (last player is environment)
        self.controls_state = [{}, {}, {}, {}, {}]

    def toggle_active_controls(self, controls_set):
        if controls_set in self.active_controls_set:
            self.active_controls_set[controls_set] = not self.active_controls_set[controls_set]
        self.refresh_active_controls()

    def refresh_active_controls(self):
        self.active_controls = []
        for key in self.active_controls_set:
            if self.active_controls_set[key]:
                for control in self.bound_controls[key]:
                    self.active_controls.append(control)

    def bind_control(self, control_name, player, target):
        """bind a control event to a target"""
        for key in self.controls:
            for control in self.controls[key]:
                if control['name'] == control_name and control['player'] == player:
                    control.update({'target': target})
                    self.bound_controls[key].append(control.copy())
        self.refresh_active_controls()

    def bind_control_switch(self, control_name, player, target):
        """bind a keyboard or joystick input state (on/off) to a target
        this function is used when the program needs to monitor the state of
        a keyboard input continuously and not only the press/release events
        """
        for key in self.controls:
            for control in self.controls[key]:
                if control['name'] == control_name and control['player'] == player:
                    if control['event_type'] == 'SWITCH':
                        control.update({'event_type': p_l.KEYUP})
                        control.update({'target': target})
                        self.bound_controls[key].append(control.copy())
                        control.update({'event_type': p_l.KEYDOWN})
                        control.update({'target': target})
                        self.bound_controls[key].append(control.copy())
                        self.controls_state[player].update({control['name']: False})
                    elif control['event_type'] == 'JOY_SWITCH':
                        control.update({'event_type': p_l.JOYBUTTONUP})
                        control.update({'target': target})
                        self.bound_controls[key].append(control.copy())
                        control.update({'event_type': p_l.JOYBUTTONDOWN})
                        control.update({'target': target})
                        self.bound_controls[key].append(control.copy())
                        self.controls_state[player].update({control['name']: False})
                    elif control['event_type'] == p_l.JOYAXISMOTION:
                        control.update({'target': target})
                        self.bound_controls[key].append(control.copy())
                        self.controls_state[player].update({control['name']: False})
        self.refresh_active_controls()


    def unbind_control(self, control_name, player, target):
        """unbind a control event from a target"""
        for key in self.bound_controls:
            for control in list(self.bound_controls[key]):
                if control['name'] == control_name and control['player'] == player and control['target'] == target:
                    self.bound_controls[key].remove(control)
            self.refresh_active_controls()
