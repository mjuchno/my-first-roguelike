# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:48:25 2019

@author: morto
"""
import tcod as libtcod

from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import save_game, load_game
from input_handlers import handle_event
from entity import get_blocking_ent_at_loc

from death_functions import kill_player, kill_monster
from render_functions import render_all, clear_all

from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from game_messages import Message
from menus import main_menu, message_box

# testing set_tile and pixel color change
import tcod.tileset
from graphics import glyph # temporary, only for tiles manipulation test
from random import randint
import time
from numpy import array

import warnings
warnings.simplefilter("default")

def main():
    constants = get_constants()
    
    # Console settings
#    console_font = 'arial10x10.png'  # old 10x10
#    console_opt = libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
#    console_font = 'Japa_20x20.png' # new 20x20
#    nb_char_horiz = 16
#    nb_char_vertic = 16
    console_font = 'Witcher_Japa_20x20.png' # new 20x20 with graphical tiles
    console_opt = libtcod.FONT_TYPE_GREYSCALE |libtcod.FONT_LAYOUT_ASCII_INROW
    nb_char_horiz = 16
    nb_char_vertic = 16+5
    libtcod.console_set_custom_font(console_font, console_opt, nb_char_horiz, nb_char_vertic)
    libtcod.sys_set_fps(constants['LIMIT_FPS'])

#    with libtcod.console_init_root(constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], 
#                                   constants['WINDOW_TITLE'], constants['FULLSCREEN'], 
#                                   constants['RENDER'], order='F', vsync=constants['VSYNC']) as root_console:
    with libtcod.console_init_root(constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], 
                                   constants['WINDOW_TITLE'], constants['FULLSCREEN'], 
                                   libtcod.RENDERER_OPENGL2, order='F', vsync=constants['VSYNC']) as root_console:
        con = libtcod.console.Console(constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], order='F')
        panel = libtcod.console.Console(constants['SCREEN_WIDTH'], constants['PANEL_HEIGHT'], order='F')
        
        player = None
        entities = []
        game_map = None
        message_log = None
        game_state = GameStates.MAIN_MENU
        
        show_main_menu = True
        show_load_error_message = False
        
        main_menu_background_image = libtcod.image_load('menu_background1.png')
        mouse = (0,0)
        
        while True:
            actions = {}
            for event in libtcod.event.wait():
                action = handle_event(event, game_state)
                actions = {**actions, **action}
            
            if show_main_menu:
                main_menu(root_console, con, main_menu_background_image, constants['SCREEN_WIDTH'],
                          constants['SCREEN_HEIGHT'])

                if show_load_error_message:
                    message_box(root_console, con, 'No save game to load', 50, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])
                    print('file not found message box')
                
                libtcod.console_flush()
    
                # Events
#                print(actions)
                new_game = actions.get('new_game')
                load_saved_game = actions.get('load_game')
                exit_game = actions.get('exit')
                
                if show_load_error_message and (new_game or load_saved_game or exit_game):
                    show_load_error_message = False
                    print('sellection after error?')
                elif new_game:
                    player, entities, game_map, message_log, game_state = get_game_variables(constants)
                    game_state = GameStates.PLAYERS_TURN
                    
                    show_main_menu = False
                    print('new_game')
                elif load_saved_game:
                    try:
                        player, entities, game_map, message_log, game_state = load_game()
                        show_main_menu = False
                    except FileNotFoundError:
                        show_load_error_message = True
                elif exit_game:
                    return True
            else:
                con.clear()
                game_ended = play_game(player, entities, game_map, message_log, game_state, root_console, con, panel, constants)
                if game_ended:
                    print('Game ended')
                    return game_ended                    
                # TODO implement return to game and main menu
                
def play_game(player, entities, game_map, message_log, game_state, root_console, con, panel, constants):
#    print(game_map.width, game_map.height)
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    mouse = (0, 0)
    
#    game_state = GameStates.PLAYERS_TURN # does this change anything ?
    previous_game_state = game_state
    targeting_item = None # is it needed ?
    animations = []

    frame = 0   
    while True:

        # testing set_tile and pixel color change
        if frame%10 == 0 and frame != 0:
            tile_set = libtcod.tileset.get_default()
            player_tile = tile_set.get_tile(glyph.GERALT_BIG.value)
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            for y in range(20):
                for x in range(20):
                    if player_tile[x][y][3] == 255:
                        player_tile[x][y][0:3] = array([r,g,b])

        
            tile_set.set_tile(glyph.GERALT_BIG.value, player_tile)
            # libtcod.tileset.set_default(tile_set) # not really needed for updating 
        frame += 1
#        print(frame)

            
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, 
                          constants['FOV_RADIUS'], constants['FOV_LIGHT_WALLS'], 
                          constants['FOV_ALGORITHM'])


        render_all(root_console, con, panel, entities, player, animations, game_map, fov_map, fov_recompute,
                   message_log, constants['BAR_WIDTH'], constants['PANEL_Y'], 
                   mouse, constants['colors'], game_state)

        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities)

        # Handling input events
        actions = {}
        if len(animations) == 0:
            for event in libtcod.event.wait():
#            for event in libtcod.event.get():
                action = handle_event(event, game_state)
                actions = {**actions, **action}
        else:
            # animations cleanup
            animations = [animation for animation in animations.copy() if animation.frames > 0]
            for event in libtcod.event.get():
                action = handle_event(event, game_state)
                actions = {**actions, **action}

        # Events
#        print(actions)
        # Window
        close_window = actions.get('close_window')
        fullscreen = actions.get('fullscreen')
        # Mouse
        mouse = actions.get('mouse')
        left_click = actions.get('left_click')
        right_click = actions.get('right_click')
        middle_click = actions.get('middle_click')
        x1_click = actions.get('x1_click')
        x2_click = actions.get('x2_click')
        # Keyboard
        exit = actions.get('exit')
        move = actions.get('move')
        wait = actions.get('wait')
        pickup = actions.get('pickup')
        show_inventory = actions.get('show_inventory')
        drop_inventory = actions.get('drop_inventory')
        text = actions.get('text')
        inventory_index = actions.get('inventory_index')
        stairs_up = actions.get('stairs_up') # not working with capslock?
        stairs_down = actions.get('stairs_down')
        level_up = actions.get('level_up')
        show_character_screen = actions.get('show_character_screen')

        
        # Player turn actions
        player_turn_results = []
        # Move
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x = player.x+dx
            dest_y = player.y+dy
            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_ent_at_loc(entities, dest_x, dest_y)
                
                if target and target.fighter and target != player:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                
#                previous_game_state = game_state # this is already known
                game_state = GameStates.ENEMY_TURN
        if wait:
            game_state = GameStates.ENEMY_TURN
        
        # Pick up
        elif pickup and game_state == GameStates.PLAYERS_TURN:

            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))
        
        # inventory
        if show_inventory:
                previous_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY
               
                
        if inventory_index != None and previous_game_state != GameStates.PLAYER_DEAD:
            if 0 <= inventory_index < len(player.inventory.items):
                item = player.inventory.items[inventory_index]
                if game_state == GameStates.SHOW_INVENTORY:
                    player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
                if game_state == GameStates.DROP_INVENTORY:
                    player_turn_results.extend(player.inventory.drop_item(item))
        
        if stairs_down and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.distance_to(player) == 0:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    con.clear()
                    
                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))
        
        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1
                
            game_state = previous_game_state
            
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN
            
        
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_result = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                       target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_result)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        # Window behaviour
        if exit:
            if close_window:
                return True
            elif game_state in (GameStates.SHOW_INVENTORY, 
                                GameStates.DROP_INVENTORY,
                                GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})    
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        # Player turn results
        for player_turn_result in player_turn_results:
#                print(player_turn_result)
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            equip = player_turn_result.get('equip')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')
            animation = player_turn_result.get('animation')
            
            if message:
                message_log.add_message(message)
            
            if animation:
                animations.append(animation)
            
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(player)
                else:
                    message = kill_monster(dead_entity)
                message_log.add_message(message)
                
            if item_added:
                entities.remove(item_added)
                previous_game_state = game_state
                game_state = GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                previous_game_state = game_state
                game_state = GameStates.ENEMY_TURN
                
            if equip:
                equip_results = player.equipment.toggle_equip(equip)
                
                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')
                    
                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))
                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))
                game_state = GameStates.ENEMY_TURN
                        
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                
                targeting_item = targeting
                
                message_log.add_message(targeting_item.item.targeting_message)
                
            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))
                
                if leveled_up:
                    message_log.add_message(Message(
                            'Your battle skills grow stronger! You reached level {0}'.format(
                            player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP
        
        # Enemy actions
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                enemy_turn_results = []
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                
                for enemy_turn_result in enemy_turn_results:
                    message = enemy_turn_result.get('message')
                    dead_entity = enemy_turn_result.get('dead')
                    animation = enemy_turn_result.get('animation')
                    
                    if animation:
                        animations.append(animation)
                
                    if message:
                        message_log.add_message(message)
                    
                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(player)
                        else:
                            message = kill_monster(dead_entity)
                        
                        message_log.add_message(message)
                        
                        if game_state == GameStates.PLAYER_DEAD:
                            break
                
                if game_state == GameStates.PLAYER_DEAD:
                    break
            else:
                previous_game_state = game_state
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()