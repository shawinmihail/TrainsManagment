# -*- coding: utf-8 -*-


def random_rule(trains):

    from random import shuffle

    trains_list = list()
    for train in trains:
        trains_list.append(train)

    shuffle(trains_list)
    return trains_list


def name_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)
    trains_list.sort(key=lambda x: x.name)
    return trains_list