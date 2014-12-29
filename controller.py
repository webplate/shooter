# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.locals as p_l
import controls


class Controller():
    """a handler for game controls"""
    def __init__(self, game):
        self.game = game
        # load static controls from controls.py
        self.controls = self.load_controls(controls.controls)
        # create empty list of bound controls (those bound in the program)
        self.bound_controls = {}
        # create empty list of active controls (those considered in main.on_event)
        self.active_controls = []
        # create a list of True/False values for active control sets
        self.active_control_set = {}
        for key in self.controls:
            self.bound_controls.update({key: []})
            self.active_control_set.update({key: False})
        # create a list of dictionaries containing control switches for each player
        # (last player is environment)
        self.controls_state = [{}, {}, {}, {}, {}]

    def load_controls(self, control_list):
        """returns a dictionary created from control_list"""
        content = {}
        # transform list in dictionaries
        key_list = ['name', 'player', 'event_type', 'event_params']
        for control_type in control_list:
            content.update({control_type: []})
            for control in control_list[control_type]:
                content_line = {}
                for i, key in enumerate(key_list):
                    content_line.update({key_list[i]: control[i]})
                content[control_type].append(content_line)
        return content

    def toggle_active_controls(self, controls_set, state):
        """toggle (on/off) a set of controls"""
        if controls_set in self.active_control_set:
            self.active_control_set[controls_set] = state
        self.refresh_active_controls()

    def refresh_active_controls(self):
        """refresh the list of active controls"""
        self.active_controls = []
        for key in self.active_control_set:
            if self.active_control_set[key]:
                for control in self.bound_controls[key]:
                    self.active_controls.append(control)

    def bind_control(self, control_name, player, target):
        """bind a control event to a target"""
        for key in self.controls:
            for control in self.controls[key]:
                if control['name'] == control_name and control['player'] == player:
                    new_ctrl = control.copy()
                    new_ctrl.update({'target': target})
                    self.bound_controls[key].append(new_ctrl)
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
                        new_ctrl = control.copy()
                        new_ctrl.update({'event_type': p_l.KEYUP})
                        new_ctrl.update({'target': target})
                        self.bound_controls[key].append(new_ctrl)
                        new_ctrl = control.copy()
                        new_ctrl.update({'event_type': p_l.KEYDOWN})
                        new_ctrl.update({'target': target})
                        self.bound_controls[key].append(new_ctrl)
                        self.controls_state[player].update({control['name']: False})
                    elif control['event_type'] == 'JOY_SWITCH':
                        new_ctrl = control.copy()
                        new_ctrl.update({'event_type': p_l.JOYBUTTONUP})
                        new_ctrl.update({'target': target})
                        self.bound_controls[key].append(new_ctrl)
                        new_ctrl = control.copy()
                        new_ctrl.update({'event_type': p_l.JOYBUTTONDOWN})
                        new_ctrl.update({'target': target})
                        self.bound_controls[key].append(new_ctrl)
                        self.controls_state[player].update({control['name']: False})
                    elif control['event_type'] == p_l.JOYAXISMOTION:
                        new_ctrl = control.copy()
                        new_ctrl.update({'target': target})
                        self.bound_controls[key].append(new_ctrl)
                        self.controls_state[player].update({control['name']: False})
        self.refresh_active_controls()

    def unbind_control(self, control_name, player, target):
        """unbind a control event from a target"""
        for key in self.bound_controls:
            for control in list(self.bound_controls[key]):
                if control['name'] == control_name and control['player'] == player and control['target'] == target:
                    self.bound_controls[key].remove(control)
            self.refresh_active_controls()

    def unbind_player(self, player):
        """unbind all controls bound to a given player"""
        for key in self.bound_controls:
            for control in list(self.bound_controls[key]):
                if control['player'] == player:
                    self.bound_controls[key].remove(control)
            self.refresh_active_controls()
