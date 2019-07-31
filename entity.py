# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 17:15:42 2019

@author: morto
"""
import tcod as libtcod
import math

from components.item import Item

from fov_functions import initialize_fov
from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, 
                 render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs = None, level=None,
                 equipment=None, equippable=None):
        self.x = x
        self.y = y
        if type(char) == int:
            self.char = chr(char)
        else:
            self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.level:
            self.level.owner = self
        if self.equipment:
            self.equipment.owner = self
        if self.equippable:
            self.equippable.owner = self
            
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        dx = int(round(dx/distance))
        dy = int(round(dy/distance))
        
        if not(game_map.is_blocked(self.x+dx, self.y+dy) or
               get_blocking_ent_at_loc(entities, self.x+dx, self.y+dy)):
            self.move(dx, dy)
    
    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = initialize_fov(game_map)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                fov.walkable[entity.x][entity.y] = False

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path.AStar(fov)
        my_path.diagonal = 1.41
        

        # Compute the path between self's coordinates and the target's coordinates
        new_path = my_path.get_path(self.x, self.y, target.x, target.y)
        
        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away

        if len(new_path) > 0 and len(new_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = new_path[0]
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

def get_blocking_ent_at_loc(entities, dest_x, dest_y):
    for entity in entities:
        if entity.blocks and entity.x == dest_x and entity.y == dest_y:
            return entity
    return None