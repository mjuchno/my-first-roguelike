# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 17:52:23 2019

@author: morto
"""
import tcod as libtcod
from random import randint

from map_objects.tile import Tile
from entity import Entity
from components.stairs import Stairs
from render_functions import RenderOrder
from game_messages import Message
from random_utils import random_choice_from_dict, from_dungeon_level
from monsters import monster_dict, spawn_monster
from items import item_dict, spawn_item

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
    def center(self):
        center_x = int((self.x1+self.x2)/2)
        center_y = int((self.y1+self.y2)/2)
        return (center_x, center_y)
    
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
#        return (self.x1+1 <= other.x2-1 and self.x2-1 >= other.x1+1 and
#                self.y1+1 <= other.y2-1 and self.y2-1 >= other.y1+1)
        
    def intersect_wall(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def create_room(self, room):
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False 
                
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1,x2), max(x1,x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1,y2), max(y1,y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            
    def place_entities(self, room, entities):
        monsters_level_table = [[2,1], [3,4], [5,6]]
        items_level_table = [[1,1], [2,4]]
        
        max_monsters_per_room = from_dungeon_level(monsters_level_table, self.dungeon_level)
        max_items_per_room = from_dungeon_level(items_level_table, self.dungeon_level)
        
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)
        
        monster_chances = {}
        for monster_type in monster_dict.keys():
            chance = monster_dict[monster_type]['chance']
            if type(chance) == list:
                chance = from_dungeon_level(chance, self.dungeon_level)
            monster_chances[monster_type] = chance

        item_chances = {}
        for item_type in item_dict.keys():
            chance = item_dict[item_type]['chance']
            if type(chance) == list:
                chance = from_dungeon_level(chance, self.dungeon_level)
            item_chances[item_type] = chance       
        
        # Monsters
        for i in range(number_of_monsters):
            x = randint(room.x1+1, room.x2-1)
            y = randint(room.y1+1, room.y2-1)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                monster = spawn_monster(monster_choice, x, y)

                if monster:        
                    entities.append(monster)
        
        # Items
        for i in range(number_of_items):
            x = randint(room.x1+1, room.x2-1)
            y = randint(room.y1+1, room.y2-1)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                item = spawn_item(item_choice, x, y)
                

                if item:
                    entities.append(item)


    def test_map(self):
        room1 = Rect(20, 20, 30, 20)
        room2 = Rect(50, 20, 10, 20)
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(room1.x2,room2.x1, 24)
        print('Room1: ',room1.center())
        print('Room2: ',room2.center())
        print('intersect: ',room1.intersect(room2))

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                 player, entities):
        rooms = []
        num_rooms = 0
        
        center_of_last_room_x = None
        center_of_last_room_y = None
        
        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)
            
            for other_room in rooms:
                if new_room.intersect(other_room):
#                    print('Room {} rejected!'.format(num_rooms+1))
                    break
            else:
                if num_rooms > 0:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                    self.place_entities(new_room, entities)
                    
                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                self.create_room(new_room)
                rooms.append(new_room)
#                print('Room {} created!'.format(num_rooms+1))
                num_rooms += 1
        
        print('Created total of {} rooms'.format(len(rooms)))
        (player.x, player.y) = rooms[0].center()
#        (npc.x, npc.y) = rooms[-1].center()

        if self.dungeon_level == 1:
            # Item at starting location
            starting_items = []
            for item_type in item_dict.keys():
                x = randint(rooms[0].x1+1, rooms[0].x2-1)
                y = randint(rooms[0].y1+1, rooms[0].y2-1)
                item = spawn_item(item_type, x, y)
#                entities.append(item)
                player.inventory.add_item(item)
                if item.equippable:
                    player.equipment.toggle_equip(item)
        
        # Stairs down
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y,
                             '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)
    
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
    
    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]
        
        self.tiles = self.initialize_tiles()
        self.make_map(constants['MAX_ROOMS'], 
                      constants['ROOM_MIN_SIZE'], constants['ROOM_MAX_SIZE'], 
                      constants['MAP_WIDTH'], constants['MAP_HEIGHT'], 
                      player, entities)
        
        player.fighter.heal(player.fighter.max_hp //2)
        
        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))
        
        return entities