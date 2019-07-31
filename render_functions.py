# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 17:30:53 2019

@author: morto
"""

import tcod as libtcod

from enum import Enum
from menus import inventory_menu, level_up_menu, character_screen
from game_states import GameStates
from animations import AnimationOrder

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def render_all(root_console, con, panel, entities, player, animations,
               game_map, fov_map, fov_recompute,
               message_log, bar_width, panel_y, mouse, colors, game_state):
    if fov_recompute:
        # Draw all tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = fov_map.fov[x][y]
                wall = game_map.tiles[x][y].block_sight
                
                if visible:
                    if wall:
                        con.bg[x][y] = colors.get('light_wall')
                    else:
                        con.bg[x][y] = colors.get('light_ground')
                    game_map.tiles[x][y].explored = True
                    
                elif game_map.tiles[x][y].explored:
                    if wall:
                        con.bg[x][y] = colors.get('dark_wall')
                    else:
                        con.bg[x][y] = colors.get('dark_ground')


    
    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)
  
    con.blit(root_console, 0, 0, 0, 0, con.width, con.height)
    
    # Panel and message log
    panel.clear(bg = libtcod.black)
    
    y = 1
    for message in message_log.messages:
        panel.print(message_log.x, y,
                    message.text, fg=message.color, 
                    bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
        y += 1
    
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    panel.print(1, 3, 'Dungeon level: {0}'.format(game_map.dungeon_level),
                fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    
    # Display entity name under cursor
    if mouse:
        panel.print(1, 0, get_names_under_mouse(mouse, entities, fov_map),
                    fg=libtcod.light_gray, 
                    bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)

    panel.blit(root_console, 0, panel_y, 0, 0, con.width, panel.height)
    
    if len(animations) > 0:
        render_animation_frame(root_console, con, animations)
    
    # Menus
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        inventory_menu(root_console, con, inventory_title,
                       player, 50, con.width, con.height)
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(root_console, con, 'Level up! Choose a stat to raise:', player, 40, con.width, con.height)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_console, player, 30, 10, con.width, con.height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
    if fov_map.fov[entity.x, entity.y] or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        con.put_char(entity.x, entity.y, ord(entity.char), libtcod.BKGND_NONE)
        con.fg[entity.x, entity.y] = entity.color

def clear_entity(con, entity):
    # erase the character that represents this object
    con.put_char(entity.x, entity.y, ord(' '), libtcod.BKGND_NONE)
    
def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = mouse
    
    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and fov_map.fov[entity.x][entity.y]]
    names = ', '.join(names)
    
    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)
    
    panel.draw_rect(x, y, total_width, 1, ord(' '), fg = None, bg = back_color, bg_blend = libtcod.BKGND_SCREEN)
    
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, ord(' '), fg = None, bg = bar_color, bg_blend = libtcod.BKGND_SCREEN)
    
    panel.print(int(x+total_width/2), y,
              '{0}: {1}/{2}'.format(name, value, maximum),
              fg=libtcod.white, 
              bg_blend=libtcod.BKGND_NONE, alignment=libtcod.CENTER)
    
def render_animation_frame(root_console, con, animations):
    for animation in animations:
        animation.play_frame(root_console)
        
#    print('before',animations)
#    animations = [animation for animation in animations.copy() if animation.frames > 0]
#    print('after',animations)