# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:21:25 2019

@author: morto
"""

import tcod as libtcod

def menu(root_console, con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = con.get_height_rect(0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console.Console(width, height, order='F')

    # print the header, with auto-wrap
    window.print_box(0, 0, width, height, header, fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.print(0, y, text, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    window.blit(root_console, x, y, 0, 0, width, height, 1.0, 0.7)


def inventory_menu(root_console, con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventoru as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)
        
    menu(root_console, con, header, options, inventory_width, screen_width, screen_height)
    
def main_menu(root_console, con, background_image, screen_width, screen_height):
    background_image.blit_2x(root_console, dest_x=0, dest_y=0)

    root_console.print_box(0, int(screen_height / 2) - 4, screen_width, 1, 
                           'TOMBS OF THE ANCIENT KINGS', 
                           fg=libtcod.yellow, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.CENTER)
    root_console.print_box(0, int(screen_height - 2), screen_width, 1, 
                           'By Morto', 
                           fg=libtcod.yellow, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.CENTER)

    menu(root_console, con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(root_console, con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(root_console, con, header, options, menu_width, screen_width, screen_height)

def character_screen(root_console, player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console.Console(character_screen_width, character_screen_height, order='F')

    window.print_box(0, 1, character_screen_width, character_screen_height, 
                     'Character Information', 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 2, character_screen_width, character_screen_height, 
                     'Level: {0}'.format(player.level.current_level), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 3, character_screen_width, character_screen_height, 
                     'Experience: {0}'.format(player.level.current_xp), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 4, character_screen_width, character_screen_height, 
                     'Experience to Level: {0}'.format(player.level.experience_to_next_level), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 6, character_screen_width, character_screen_height, 
                     'Maximum HP: {0}'.format(player.fighter.max_hp), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 7, character_screen_width, character_screen_height, 
                     'Attack: {0}'.format(player.fighter.power), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)
    window.print_box(0, 8, character_screen_width, character_screen_height, 
                     'Defense: {0}'.format(player.fighter.defense), 
                     fg=libtcod.white, bg_blend=libtcod.BKGND_NONE, alignment=libtcod.LEFT)

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    window.blit(root_console, x, y, 0, 0, character_screen_width, character_screen_height, 1.0, 0.7)

def message_box(root_console, con, header, width, screen_width, screen_height):
    menu(root_console, con, header, [], width, screen_width, screen_height)