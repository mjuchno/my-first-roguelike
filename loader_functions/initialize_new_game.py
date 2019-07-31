# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 16:37:18 2019

@author: morto
"""

import tcod as libtcod

from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from graphics import glyph # this shouldn't be a component !!!

from render_functions import RenderOrder

from map_objects.game_map import GameMap

from game_states import GameStates
from game_messages import MessageLog



def get_constants():
    
    WINDOW_TITLE = 'Witcher RL'
    
    SCREEN_WIDTH = int(1920/20/1)
    SCREEN_HEIGHT = int(1080/20/1)-4
    
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50
    print('SCREEN SIZE: {} x {}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
    
    BAR_WIDTH = 20
    PANEL_HEIGHT = 5
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
    
    MESSAGE_X = BAR_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - MESSAGE_X
    MESSAGE_HEIGHT = PANEL_HEIGHT - 1
    
    MAP_WIDTH = SCREEN_WIDTH
    MAP_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT
    MAX_ROOMS = 10
    
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    
    MAX_MONSTERS_PER_ROOM = 4
    MAX_ITEMS_PER_ROOM = 5
    
    RENDER = libtcod.RENDERER_SDL2
#    RENDER = libtcod.RENDERER_OPENGL2

    FULLSCREEN = False
    VSYNC = False
    LIMIT_FPS = 20  #20 frames-per-second maximum
    
    FOV_ALGORITHM = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    colors = {
            'dark_wall': libtcod.Color(0, 0, 100),
            'dark_ground': libtcod.Color(50, 50, 150),
            'light_wall': libtcod.Color(130, 110, 50),
            'light_ground': libtcod.Color(200, 180, 50)
            }

    constants = {
        'WINDOW_TITLE': WINDOW_TITLE,
        'LIMIT_FPS': LIMIT_FPS,
        'VSYNC': VSYNC,
        'RENDER': RENDER,
        'FULLSCREEN': FULLSCREEN,
        'SCREEN_WIDTH': SCREEN_WIDTH,
        'SCREEN_HEIGHT': SCREEN_HEIGHT,
        'BAR_WIDTH': BAR_WIDTH,
        'PANEL_HEIGHT': PANEL_HEIGHT,
        'PANEL_Y': PANEL_Y,
        'MESSAGE_X': MESSAGE_X,
        'MESSAGE_WIDTH': MESSAGE_WIDTH,
        'MESSAGE_HEIGHT': MESSAGE_HEIGHT,
        'MAP_WIDTH': MAP_WIDTH,
        'MAP_HEIGHT': MAP_HEIGHT,
        'ROOM_MAX_SIZE': ROOM_MAX_SIZE,
        'ROOM_MIN_SIZE': ROOM_MIN_SIZE,
        'MAX_ROOMS': MAX_ROOMS,
        'FOV_ALGORITHM': FOV_ALGORITHM,
        'FOV_LIGHT_WALLS': FOV_LIGHT_WALLS,
        'FOV_RADIUS': FOV_RADIUS,
        'MAX_MONSTERS_PER_ROOM': MAX_MONSTERS_PER_ROOM,
        'MAX_ITEMS_PER_ROOM': MAX_ITEMS_PER_ROOM,
        'colors': colors
            }
    
    return constants

def get_game_variables(constants):
    # Entities
    fighter_component = Fighter(hp=100, defense=1, power=4)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
#    player = Entity(0, 0 , '@', libtcod.white, 'Morto', blocks=True, 
#                    render_order=RenderOrder.ACTOR, fighter=fighter_component,
#                    inventory=inventory_component, level=level_component)
    

    player = Entity(0, 0 , glyph.GERALT_BIG.value, libtcod.white, 'Morto', blocks=True, 
                    render_order=RenderOrder.ACTOR, fighter=fighter_component,
                    inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]
    
    # Map
    game_map = GameMap(constants['MAP_WIDTH'], constants['MAP_HEIGHT'])
    game_map.make_map(constants['MAX_ROOMS'], 
                      constants['ROOM_MIN_SIZE'], constants['ROOM_MAX_SIZE'], 
                      constants['MAP_WIDTH'], constants['MAP_HEIGHT'], 
                      player, entities)

    message_log = MessageLog(constants['MESSAGE_X'], constants['MESSAGE_WIDTH'], constants['MESSAGE_HEIGHT'])
    game_state = GameStates.PLAYERS_TURN
    
    return player, entities, game_map, message_log, game_state