# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 20:56:25 2019

@author: morto
"""

import tcod as libtcod
import tcod.event
from game_states import GameStates

def handle_event(event, game_state):
#    print(event, game_state)
    if event.type == "QUIT":
        return {'exit': True, 'close_window' : True}
    elif event.type == "KEYDOWN":
        # different than in tutorial
        if game_state == GameStates.PLAYERS_TURN:
            return handle_keydown(event)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keydown(event)
        elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            return handle_inventory_keydown(event)
        elif game_state == GameStates.TARGETING:
            return handle_targeting_keys(event)
        elif game_state == GameStates.MAIN_MENU:
            return handle_main_menu_keys(event)
        elif game_state == GameStates.LEVEL_UP:
            return handle_level_up_menu(event)
        elif game_state == GameStates.CHARACTER_SCREEN:
            return handle_character_screen(event)
    elif event.type =='TEXTINPUT':
        if game_state in (GameStates.SHOW_INVENTORY, 
                          GameStates.DROP_INVENTORY
                          ):
            return {'inventory_index': ord(event.text)-ord('a')}
        else:
            return {'text': event.text}
    elif event.type == "MOUSEBUTTONDOWN":
        return handle_mouse_button(event)
    elif event.type == "MOUSEMOTION":
        return {'mouse': (event.tile.x, event.tile.y)}
    elif event.type == "MOUSEWHEEL":
        return {'wheel': (event.x, event.y)}
    else:
#        print(event)
        return {}

def handle_keydown(event):
#    # Movement keys
#    print(event, event.sym)
    if event.sym == tcod.event_constants.K_UP or event.sym == tcod.event_constants.K_KP_8:
        return {'move': (0, -1)}
    elif event.sym == tcod.event_constants.K_DOWN or event.sym == tcod.event_constants.K_KP_2:
        return {'move': (0, 1)}
    elif event.sym == tcod.event_constants.K_LEFT or event.sym == tcod.event_constants.K_KP_4:
        return {'move': (-1, 0)}
    elif event.sym == tcod.event_constants.K_RIGHT or event.sym == tcod.event_constants.K_KP_6:
        return {'move': (1, 0)}
    elif event.sym == tcod.event_constants.K_KP_5 or event.sym == tcod.event_constants.K_CLEAR:
#        return {'move': (0, 0)}
        return {'wait': True}
    
    elif event.sym == tcod.event_constants.K_KP_7:
        return {'move': (-1, -1)}
    elif event.sym == tcod.event_constants.K_KP_9:
        return {'move': (1, -1)}
    elif event.sym == tcod.event_constants.K_KP_1:
        return {'move': (-1, 1)}
    elif event.sym == tcod.event_constants.K_KP_3:
        return {'move': (1, 1)}
    
    # Stairs
    elif event.sym == tcod.event_constants.K_COMMA and event.mod in [
            tcod.event_constants.KMOD_RSHIFT|tcod.event_constants.KMOD_NUM, 
            tcod.event_constants.KMOD_RSHIFT]:
        return {'stairs_up': True}
    elif event.sym == tcod.event_constants.K_PERIOD and event.mod in [
            tcod.event_constants.KMOD_RSHIFT|tcod.event_constants.KMOD_NUM, 
            tcod.event_constants.KMOD_RSHIFT]:
        return {'stairs_down': True}
    
    # Action keys
    elif event.sym == tcod.event_constants.K_g:
        return {'pickup': True}
    elif event.sym == tcod.event_constants.K_c:
        return {'show_character_screen': True}
    
    # Menu keys
    elif event.sym == tcod.event_constants.K_i:
        return {'show_inventory': True}
    elif event.sym == tcod.event_constants.K_d:
        return {'drop_inventory': True}

    # Alt+Enter: toggle full screen
    elif (event.sym == tcod.event_constants.K_RETURN and 
          event.mod in [tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL,
                        tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL|tcod.event_constants.KMOD_NUM
                        ]):
        return {'fullscreen': True}

    elif event.sym == tcod.event_constants.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_player_dead_keydown(event):
    # Menu keys
    if event.sym == tcod.event_constants.K_i:
        return {'show_inventory': True}

    elif (event.sym == tcod.event_constants.K_RETURN and 
          event.mod in [tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL,
                        tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL|tcod.event_constants.KMOD_NUM
                        ]):
#        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif event.sym == tcod.event_constants.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_inventory_keydown(event):
    if (event.sym == tcod.event_constants.K_RETURN and 
          event.mod in [tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL,
                        tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL|tcod.event_constants.KMOD_NUM
                        ]):
#        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif event.sym == tcod.event_constants.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_targeting_keys(event):
    if (event.sym == tcod.event_constants.K_RETURN and 
          event.mod in [tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL,
                        tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL|tcod.event_constants.KMOD_NUM
                        ]):
#        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif event.sym == tcod.event_constants.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_mouse_button(event):
    if event.button == tcod.event.BUTTON_LEFT:
        return {'left_click': (event.tile.x, event.tile.y)}
    elif event.button == tcod.event.BUTTON_RIGHT:
        return {'right_click': (event.tile.x, event.tile.y)}
    elif event.button == tcod.event.BUTTON_MIDDLE:
        return {'middle_click': (event.tile.x, event.tile.y)}
    elif event.button == tcod.event.BUTTON_X1:
        return {'x1_click': (event.tile.x, event.tile.y)}        
    elif event.button == tcod.event.BUTTON_X2:
        return {'x2_click': (event.tile.x, event.tile.y)}        
    else:
        return {}
    
def handle_main_menu_keys(event):
    if event.sym == tcod.event_constants.K_a:
        return {'new_game': True}
    elif event.sym == tcod.event_constants.K_b:
        return {'load_game': True}
    elif event.sym == tcod.event_constants.K_c:
        return {'exit': True}
    
    elif (event.sym == tcod.event_constants.K_RETURN and 
          event.mod in [tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL,
                        tcod.event_constants.KMOD_RALT|tcod.event_constants.KMOD_LCTRL|tcod.event_constants.KMOD_NUM
                        ]):
#        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif event.sym == tcod.event_constants.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_level_up_menu(event):
    if event.sym == tcod.event_constants.K_a:
        return {'level_up': 'hp'}
    elif event.sym == tcod.event_constants.K_b:
        return {'level_up': 'str'}
    elif event.sym == tcod.event_constants.K_c:
        return {'level_up': 'def'}
    
    return {}

def handle_character_screen(event):
    if event.sym == tcod.event_constants.K_ESCAPE:
        return {'exit': True}
    return {}