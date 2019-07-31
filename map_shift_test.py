# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:10:16 2019

@author: mjuchno
"""

class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight
        self.explored = False
        

class GameMap:
    def __init__(self, width, height, map_array=None):
        self.width = width
        self.height = height
        if map_array:
            self.tiles = self.combine_maps(map_array)
        else:
            self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def combine_maps(map_array):
        for map_row in map_array:
            for map_col in map_row:
                pass

map1 = GameMap(3,3)
map2 = GameMap(3,3)
map3 = GameMap(3,3)
big_map = GameMap(3,9)
