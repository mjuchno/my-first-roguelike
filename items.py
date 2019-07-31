# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 21:09:13 2019

@author: morto
"""

import tcod as libtcod

from components.item import Item
from components.equippable import Equippable
from item_functions import heal, cast_lightning, cast_fireball, cast_confusion
from entity import Entity
from game_messages import Message
from graphics import glyph
from render_functions import RenderOrder
from equipment_slot import EquipmentSlot

from Color import GColor

item_dict = {
        'HEALING_POTION': {'name': 'Healing Potion',
                   'glyph': glyph.POTION,
                   'ascii': '!',
                   'ascii_color': libtcod.violet,
                   'use_function': heal,
                   'use_fun_param': {
                           'amount': 40
                           },
                   'chance': 35
                   },
        'FIREBALL_SCROLL': {'name': 'Fireball scroll',
                   'glyph': None,
                   'ascii': '#',
                   'ascii_color': libtcod.red,
                   'use_function': cast_fireball,
                   'use_fun_param': {
                           'targeting': True,
                           'targeting_message': Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                           'damage': 25,
                           'radius': 3,
                           },
                   'chance': [[25, 6]]
                   },
        'LIGHTNING_SCROLL': {'name': 'Lightning scroll',
                   'glyph': None,
                   'ascii': '#',
                   'ascii_color': libtcod.yellow,
                   'use_function': cast_lightning,  
                   'use_fun_param': {
                           'damage': 40,
                           'maximum_range': 5,
                           },
                   'chance': [[25, 4]]
                   },
        'CONFUSION_SCROLL': {'name': 'Confusion scroll',
                   'glyph': None,
                   'ascii': '#',
                   'ascii_color': libtcod.pink,
                   'use_function': cast_confusion,
                   'use_fun_param': {
                           'targeting': True,
                           'targeting_message': Message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan),
                           },
                   'chance': [[10, 2]]
                   },
        'PRACTICE_SWORD': {'name': 'Practice sword',
                   'glyph': None,
                   'ascii': '/',
                   'ascii_color': libtcod.dark_sky,
                   'equippable': True,
                   'equip_param': {
                           'slot': EquipmentSlot.MAIN_HAND,
                           'power_bonus': 1
                           },
                   'chance': [[0, 1]]
                   },
        'PRACTICE_SHIELD': {'name': 'Practice shield',
                   'glyph': None,
                   'ascii': '[',
                   'ascii_color': libtcod.darker_orange,
                   'equippable': True,
                   'equip_param': {
                           'slot': EquipmentSlot.OFF_HAND,
                           'defense_bonus': 1
                           },
                   'chance': [[0, 1]]
                   }
        }


def spawn_item(item_type, x, y, idict=item_dict, use_glyphs=True):
    equipment_component = None
    item_component = None
    
    item_name = idict[item_type]['name']
    if idict[item_type]['glyph'] and use_glyphs:
        glyph = idict[item_type]['glyph'].value
        color = idict[item_type]['ascii_color']  # or libtcod.white if has it's own color?
    else:
        glyph = idict[item_type]['ascii']
        color = idict[item_type]['ascii_color']
   
    # Defining item_component based on use_function
    use_function = idict[item_type].get('use_function')
    if use_function:
       use_fun_param = idict[item_type].get('use_fun_param')
       item_component = Item(use_function=use_function, **use_fun_param)

    # Defining equippable compoment based on equip_param, 'equippable' could be removed?
    equippable = idict[item_type].get('equippable')
    if equippable:
        equip_param = idict[item_type].get('equip_param')
        equipment_component = Equippable(**equip_param)
        
    # Creating an item
    item = Entity(x, y, glyph, color, item_name, 
                  blocks=False, render_order=RenderOrder.ITEM, 
                  item=item_component, equippable=equipment_component)
    return item
