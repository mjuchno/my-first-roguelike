# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:50:46 2019

@author: mjuchno
"""

stat_list = [x for x in range(1,21)]

def move(stat):
    base_energy = 100
    if stat < 5:
        energy_bonus = (5-stat)*15
    elif 5 <= stat <= 10:
        energy_bonus = (5-stat)*10
    elif 10 < stat <= 15:
        energy_bonus = (10-stat)*5-50
    elif stat > 15:
        energy_bonus = (15-stat)-75
    cost = base_energy + energy_bonus
    return (cost, cost/base_energy)

for stat in stat_list:
    print(stat, move(stat))