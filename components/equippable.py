# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 19:52:29 2019

@author: morto
"""

class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus