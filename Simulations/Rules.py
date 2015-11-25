# -*- coding: utf-8 -*-


def faster_ready_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)

    trains_list.sort(key=lambda tr: tr.ready_time)
    return trains_list


def random1_rule(trains):

    from random import shuffle

    trains_list = list()
    for train in trains:
        trains_list.append(train)

    shuffle(trains_list)
    return trains_list


def random2_rule(trains):

    from random import shuffle

    trains_list = list()
    for train in trains:
        trains_list.append(train)

    shuffle(trains_list)
    return trains_list


def random3_rule(trains):

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


def short_first_way_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)
    trains_list.sort(key=lambda x: x.position.ways[0].time_to_pass)
    return trains_list


def short_sum_ways_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)
    trains_list.sort(key=lambda x: x.ways_time_sum())
    return trains_list


def long_first_way_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)
    trains_list.sort(key=lambda x: x.position.ways[0].time_to_pass)
    trains_list.reverse()
    return trains_list


def long_sum_ways_rule(trains):

    trains_list = list()
    for train in trains:
        trains_list.append(train)
    trains_list.sort(key=lambda x: x.ways_time_sum())
    trains_list.reverse()
    return trains_list


rules_dict = dict()
rules_dict[long_sum_ways_rule.__name__] = long_sum_ways_rule
rules_dict[random1_rule.__name__] = random1_rule
rules_dict[random2_rule.__name__] = random2_rule
rules_dict[random3_rule.__name__] = random3_rule
rules_dict[name_rule.__name__] = name_rule
rules_dict[short_first_way_rule.__name__] = short_first_way_rule
rules_dict[short_sum_ways_rule.__name__] = short_sum_ways_rule
rules_dict[long_first_way_rule.__name__] = long_first_way_rule
rules_dict[faster_ready_rule.__name__] = faster_ready_rule