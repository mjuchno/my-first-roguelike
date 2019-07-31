# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 21:20:18 2019

@author: morto
"""

from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
    TARGETING = 6
    MAIN_MENU = 7
    LEVEL_UP = 8
    CHARACTER_SCREEN = 9