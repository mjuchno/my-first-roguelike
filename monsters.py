# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 21:49:43 2019

@author: morto
"""


import tcod as libtcod

from graphics import glyph
from entity import Entity
from components.fighter import Fighter
from components.ai import BasicMonster
from render_functions import RenderOrder
from Color import GColor

monster_dict = {
        'NEKKER': {'name': 'nekker',
                   'glyph': glyph.NEKKER,
                   'ascii': 'n',
                   'ascii_color': libtcod.light_magenta,
                   'hp': 20,
                   'defense': 0,
                   'power': 4,
                   'xp': 35,
                   'chance': [[50, 1], [30, 3], [0, 5]]
                   },
       
        'NEKKER_W': {'name': 'nekker warrior',
                   'glyph': glyph.NEKKER_W,
                   'ascii': 'n',
                   'ascii_color': libtcod.dark_red,
                   'hp': 25,
                   'defense': 0,
                   'power': 5,
                   'xp': 40,
                   'chance': [[20, 2], [30, 3]]
                   },
                     
        'WILD_BOAR': {'name': 'wild boar',
                   'glyph': glyph.WILD_BOAR,
                   'ascii': 'w',
                   'ascii_color': libtcod.dark_sepia,
                   'hp': 25,
                   'defense': 0,
                   'power': 4,
                   'xp': 35,
                   'chance': [[30, 1], [20, 2], [10, 5]]
                   },
        
        'BANSHEE': {'name': 'banshee',
                   'glyph': glyph.BANSHEE,
                   'ascii': 'b',
                   'ascii_color': libtcod.sepia,
                   'hp': 30,
                   'defense': 1,
                   'power': 6,
                   'xp': 60,
                   'chance': [[15, 3], [30, 5], [50, 7]]
                   },

        'WEREWOLF': {'name': 'werewolf',
                   'glyph': glyph.WEREWOLF,
                   'ascii': 'W',
                   'ascii_color': libtcod.darker_red,
                   'hp': 40,
                   'defense': 0,
                   'power': 6,
                   'xp': 60,
                   'chance': [[15, 4], [30, 6], [50, 8]]
                   },
        
        'GRIFFIN': {'name': 'griffin',
                   'glyph': glyph.GRIFFIN,
                   'ascii': 'G',
                   'ascii_color': libtcod.dark_azure,
                   'hp': 40,
                   'defense': 2,
                   'power': 8,
                   'xp': 100,
                   'chance': [[15, 5], [30, 7]]
                   },
                
        'GARGOYL': {'name': 'gargoyl',
                   'glyph': glyph.GARGOYL,
                   'ascii': 'G',
                   'ascii_color': libtcod.lightest_grey,
                   'hp': 50,
                   'defense': 3,
                   'power': 7,
                   'xp': 100,
                   'chance': [[15, 6], [30, 8]]
                   },
                    
        'FIELD': {'name': 'fiend',
                   'glyph': glyph.FIEND,
                   'ascii': 'F',
                   'ascii_color': libtcod.red,
                   'hp': 60,
                   'defense': 3,
                   'power': 12,
                   'xp': 150,
                   'chance': [[15, 7], [30, 9]]
                   },
                         
        'ULFHEDINN': {'name': 'Ulfhedinn',
                   'glyph': glyph.ULFHEDINN,
                   'ascii': 'W',
                   'ascii_color': libtcod.lighter_han,
                   'hp': 60,
                   'defense': 0,
                   'power': 10,
                   'xp': 150,
                   'chance': [[15, 8], [30, 10]]
                   },
                     
        'LESHy': {'name': 'leshy',
                   'glyph': glyph.LESHY,
                   'ascii': 'L',
                   'ascii_color': libtcod.darker_green,
                   'hp': 60,
                   'defense': 4,
                   'power': 8,
                   'xp': 150,
                   'chance': [[15, 9], [30, 11]]
                   },
                      
        'TEST_MONSTER': {'name': 'test monster',
                   'glyph': glyph.GERALT,
                   'ascii': '@',
                   'ascii_color': libtcod.red,
                   'hp': 1,
                   'defense': -1,
                   'power': -1,
                   'xp': -1,
                   'chance': 0
                   },
                         
        'TEST_MONSTER': {'name': 'test monster',
                   'glyph': glyph.GERALT,
                   'ascii': '@',
                   'ascii_color': libtcod.red,
                   'hp': 1,
                   'defense': -1,
                   'power': -1,
                   'xp': -1,
                   'chance': 0
                   }

        }

monster_param_list = ['name', 'glyph', 'ascii', 'ascii_color',
                      'hp','defense','power','xp','chance']

def test_monster_dict(mdict, vlist):
    print('{:15s} | {:15s} | {:1s} | {:3s} | {:3s} | {:3s} | {:3s} | {:15s} | {:15s}'.format('monster_type',
              'GLYPH', GColor.RGB(255,255,255)+'@'+GColor.END,
              ' hp', 'def', 'pow', ' xp', 'name', '[chance, level]'))
    for monster_type in monster_dict.keys():
        for param in vlist:
            try:
                test = mdict[monster_type][param]
            except:
                print('Error in monster: {}, parameter {}'.format(monster_type, param))
        glyph = mdict[monster_type]['glyph']
        aglyph = mdict[monster_type]['ascii']
        color = mdict[monster_type]['ascii_color']
        hp = mdict[monster_type]['hp']
        defense = mdict[monster_type]['defense']
        power = mdict[monster_type]['power']
        xp = mdict[monster_type]['xp']
        chance = mdict[monster_type]['chance']
        name = mdict[monster_type]['name']
        if glyph:
            glyph_name = glyph.name
        else:
            glyph_name = '_None_'
        print('{:15s} | {:15s} | {:1s} | {:3d} | {:3d} | {:3d} | {:3d} | {:15s} | {:15s}'.format(monster_type,
              GColor.RGB(*color)+glyph_name.ljust(15)+GColor.END,
              GColor.RGB(*color)+aglyph+GColor.END,
              hp, defense, power, xp, name, str(chance)))
            

def spawn_monster(monster_type, x, y, mdict=monster_dict, use_glyphs=True):
    ai_component = BasicMonster()
    fighter_component = Fighter(hp=mdict[monster_type]['hp'], 
                                defense=mdict[monster_type]['defense'], 
                                power=mdict[monster_type]['power'], 
                                xp=mdict[monster_type]['xp'])
    name = mdict[monster_type]['name']
    if mdict[monster_type]['glyph'] and use_glyphs:
        glyph = mdict[monster_type]['glyph'].value
        color = libtcod.white
    else:
        glyph = ord(mdict[monster_type]['ascii'])
        color = mdict[monster_type]['ascii_color']
    
    monster = Entity(x, y, glyph, color, name, blocks=True,
                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
    
    return monster

if __name__ == '__main__':
    test_monster_dict(monster_dict, monster_param_list)





