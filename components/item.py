# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 12:20:19 2019

@author: morto
"""

class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
        