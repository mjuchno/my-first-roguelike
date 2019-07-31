# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:56:07 2019

@author: morto
"""
import os
import shelve

def save_game(player, entities, game_map, message_log, game_state, file_name='save_game'):
    with shelve.open(file_name, 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        
def load_game(file_name='save_game'):
    if not os.path.isfile(file_name+'.dat'):
        raise FileNotFoundError
    
    with shelve.open(file_name, 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        
    player = entities[player_index]
    
    return player, entities, game_map, message_log, game_state
