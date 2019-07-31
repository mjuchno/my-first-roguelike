# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 17:22:07 2019

@author: morto
"""

import tcod as libtcod

from enum import Enum
from numpy import array, int8
from math import pi, sin, sqrt

class AnimationOrder(Enum):
    ENVIRONMENT = 1
    OBJECTS = 2
    PARTICLES = 3
    AREA_EFFECTS = 4

class FireBallBlast:
    def __init__(self, x, y, radius=3, frames=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.frames = frames
        self.total_frames = frames
        self.order = AnimationOrder.AREA_EFFECTS
        
    def play_frame(self, con):
        new_color = array(libtcod.red)
        key_color = libtcod.magenta
        # new console and blitting with alpha
        a = (self.total_frames-self.frames)/self.total_frames
        anim_con = libtcod.console.Console(2*self.radius+1,2*self.radius+1, order='F')
        for y in range(anim_con.height):
            for x in range(anim_con.width):
                if int(sqrt((self.radius-x)**2+(self.radius-y)**2)) <= self.radius:
                    anim_con.bg[x,y] = new_color
                else:
                    anim_con.bg[x,y] = key_color
        anim_con.blit(con, dest_x=self.x-self.radius, dest_y=self.y-self.radius, 
                      src_x=0, src_y=0, width=0, height=0, 
                      fg_alpha=1.0, bg_alpha=a, key_color=key_color)
        self.frames -= 1
        

class HealingLight:
    def __init__(self, target, frames=10):
        self.target = target
        self.frames = frames
        self.total_frames = frames
        self.order = AnimationOrder.AREA_EFFECTS
        
    @property
    def x(self):
        return self.target.x
    
    @property
    def y(self):
        return self.target.y
        
    def play_frame(self, con):
        new_color = array(libtcod.violet)
        # Changing directly a con.bg color
#        bg_color = con.bg[self.x][self.y]
#        a = (self.total_frames-self.frames)/self.total_frames
#        color = int8(bg_color+(new_color-bg_color)*sin(pi*a))
#        con.bg[self.x][self.y] = color
        # new console and blitting with alpha
        a = (self.total_frames-self.frames)/self.total_frames
        anim_con = libtcod.console.Console(1,1, order='F')
        anim_con.bg[0,0] = new_color
        anim_con.blit(con, dest_x=self.x, dest_y=self.y, src_x=0, src_y=0, width=0, height=0, fg_alpha=1.0, bg_alpha=a)

        self.frames -= 1
        
class ConfusionLight:
    def __init__(self, target, frames=10):
        self.target = target
        self.frames = frames
        self.total_frames = frames
        self.order = AnimationOrder.AREA_EFFECTS
        
    @property
    def x(self):
        return self.target.x
    
    @property
    def y(self):
        return self.target.y
        
    def play_frame(self, con):
        new_color = array(libtcod.pink)
        # Changing directly a con.bg color
#        bg_color = con.bg[self.x][self.y]
#        a = (self.total_frames-self.frames)/self.total_frames
#        color = int8(bg_color+(new_color-bg_color)*sin(pi*a))
#        con.bg[self.x][self.y] = color
        # new console and blitting with alpha
        a = (self.total_frames-self.frames)/self.total_frames
        anim_con = libtcod.console.Console(1,1, order='F')
        anim_con.bg[0,0] = new_color
        anim_con.blit(con, dest_x=self.x, dest_y=self.y, src_x=0, src_y=0, width=0, height=0, fg_alpha=1.0, bg_alpha=a)
        
        self.frames -= 1
        
class LightningFlash:
    def __init__(self, target, frames=10):
        self.target = target
        self.frames = frames
        self.total_frames = frames
        self.order = AnimationOrder.AREA_EFFECTS
        
    @property
    def x(self):
        return self.target.x
    
    @property
    def y(self):
        return self.target.y
        
    def play_frame(self, con):
        new_color = array(libtcod.yellow)
        # Changing directly a con.bg color
#        bg_color = con.bg[self.x][self.y]
#        a = (self.total_frames-self.frames)/self.total_frames
#        color = int8(bg_color+(new_color-bg_color)*sin(pi*a))
#        con.bg[self.x][self.y] = color
        # new console and blitting with alpha
        a = (self.total_frames-self.frames)/self.total_frames
        anim_con = libtcod.console.Console(1,1, order='F')
        anim_con.bg[0,0] = new_color
        anim_con.blit(con, dest_x=self.x, dest_y=self.y, src_x=0, src_y=0, width=0, height=0, fg_alpha=1.0, bg_alpha=a)
        

        self.frames -= 1