# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 20:57:36 2019

@author: morto
"""

import tcod as libtcod

from game_messages import Message
from components.ai import ConfusedMonster
from animations import FireBallBlast, HealingLight, LightningFlash, ConfusionLight

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')
    
    results = []
    
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        animation = HealingLight(entity)
        results.append({'animation': animation,
                        'consumed': True,
                        'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    
    results = []
    
    target = None
    closes_distance = maximum_range + 1
    
    for entity in entities:
        if entity.fighter and entity != caster and fov_map.fov[entity.x][entity.y]:
            distance = caster.distance_to(entity)
            if distance < closes_distance:
                target = entity
                closes_distance = distance
    
    if target:
        animation = LightningFlash(target)
        results.append({'animation': animation,
                        'consumed': True, 'target': target, 
                        'message': Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage)) })
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})
        
    return results

def cast_fireball(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    
    results = []
    
    if not fov_map.fov[target_x][target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results
    animation = FireBallBlast(target_x, target_y, radius)
    results.append({'animation': animation,
                    'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))
            
#    print(results)
    return results

def cast_confusion(*arg, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    
    results = []
    
    if not fov_map.fov[target_x][target_y]:
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results
    
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            animation = ConfusionLight(entity)
            
            confused_ai = ConfusedMonster(entity.ai, animation, 10)
            
            confused_ai.owner = entity
            entity.ai = confused_ai
            
            
            results.append({'animation': animation,
                            'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), libtcod.light_green)})
            
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})
        
    return results