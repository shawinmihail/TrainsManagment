# -*- coding: utf-8 -*-
from random import random


def launch_cost_func(route): return (1000 + 75 * len(route)) * (2+random())


def storage_cost_func(): return 5 + random() * 5


def growth_coef_func(): return 4 * (random() * random()) + 2 * random() + 0.5


def time_distance_func(): return 0.2 * random() + 0.03


def period_func(): return 5 + int(random() * 16)


def get_random_element(list1):
    index = int(random() * len(list1)) + 1
    return list1[index]