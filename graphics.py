# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 16:02:06 2019

@author: morto
"""

from enum import Enum

class glyph(Enum):
    # place-holders
    NONE = ord('?')
    POTION = 10*16 + 13 # before ord('!'), now upside down BUT HAS TO BE SUPPORTED BY FONT!
    SCROLL = ord('#')
    
    # graphical tiles
    GERALT_OLD = 255 + 0*16 + 1
    YENNEFER = 255 + 0*16 + 2
    BARON = 255 + 0*16 + 3
    TRIS = 255 + 0*16 + 4
    JASKIER = 255 + 0*16 + 5
    YARPEN_BIG = 255 + 0*16 + 6
    
    FIEND = 255 + 1*16 + 1
    NEKKER = 255 + 1*16 + 2
    DROWNER_1 = 255 + 1*16 + 3
    WATER_HAG_1 = 255 + 1*16 + 4
    SIREN = 255 + 1*16 + 5
    YARPEN = 255 + 1*16 + 6
    
    DROWNER_2 = 255 + 2*16 + 1
    BRUXA = 255 + 2*16 + 2
    ALP = 255 + 2*16 + 3
    WATER_HAG_2 = 255 + 2*16 + 4
    FLEDER = 255 + 2*16 + 5
    CIRI = 255 + 2*16 + 6
    
    GRIFFIN = 255 + 3*16 + 1
    LESHY = 255 + 3*16 + 2
    GARGOYL = 255 + 3*16 + 3
    LONGLOCK = 255 + 3*16 + 4
    BANSHEE = 255 + 3*16 + 5
    GERALT = 255 + 3*16 + 6
    
    NEKKER_W = 255 + 4*16 + 1
    WILD_BOAR = 255 + 4*16 + 2
    WEREWOLF = 255 + 4*16 + 3
    ULFHEDINN = 255 + 4*16 + 4
#    JASKIER = 255 + 4*16 + 5
    GERALT_BIG = 255 + 4*16 + 6