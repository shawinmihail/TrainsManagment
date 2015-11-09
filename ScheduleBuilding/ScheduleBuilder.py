# -*- coding: utf-8 -*-
from ScheduleBuilding.Rules import *
from gui.GantDiagrammCreator import *
from ScheduleBuilding.ConfigurationParser import ConfigurationParser
from ScheduleBuilding.ConfigurationGenerator import ConfigurationGenerator
from datetime import datetime


class ScheduleBuilder:

    MIN_TRAINS_DELAY = 15

    @staticmethod
    def find_shift(trains_above, train):
        for other_train in trains_above:
            own_schedule = train.schedule
            other_schedule = other_train.schedule
            t_lim = min(len(own_schedule), len(other_schedule))
            for t in range(t_lim):
                own_position = own_schedule[t]
                other_position = other_schedule[t]
                own_way = own_position.way()
                other_way = other_position.way()
                if own_way == other_way and own_way is not None:
                    own_dispatch = own_position.dispatch()
                    other_dispatch = other_position.dispatch()
                    if own_dispatch == other_dispatch:
                        own_time_in_way = own_position.time_in_way
                        other_time_in_way = other_position.time_in_way
                        delay = own_time_in_way - other_time_in_way
                        # check conflicts with stations windows
                        for close_time in own_dispatch.close_times:
                            arrival_time = own_position.find_time_of_current_destination_arrival()
                            if close_time[0] < arrival_time < close_time[1]:
                                shift = arrival_time - close_time[0]
                                return shift
                        # check conflict with another trains
                        if abs(delay) < ScheduleBuilder.MIN_TRAINS_DELAY:
                            shift = ScheduleBuilder.MIN_TRAINS_DELAY - delay
                            return shift

        return None

    @staticmethod
    def make_schedule(scheme, rule):
        trains_above = list()
        trains_by_priority = rule(scheme.trains)
        shifts_above = list()
        for train in trains_by_priority:
            shift = ScheduleBuilder.simulate_train(scheme, trains_above, shifts_above, train, 0)
            shifts_above.append(shift)
            trains_above.append(train)

        # for train in trains_by_priority:
        #     print(train.schedule)

    @staticmethod
    def simulate_train(scheme, trains_above, shifts_above, next_train, next_shift):
        scheme.reset()
        # simulate trains above
        while not ScheduleBuilder.trains_has_arrived(trains_above + [next_train]):
            t = scheme.current_time

            # launch trains above with calculated shift
            for train, shift in zip(trains_above, shifts_above):
                if t >= shift:
                    train.launch()

            # launch next train
            if t >= next_shift:
                next_train.launch()

            scheme.tick()

        # sum shift while there not will be conflicts
        additional_shift = ScheduleBuilder.find_shift(trains_above, next_train)
        if additional_shift is None:
            return next_shift
        else:
            return ScheduleBuilder.simulate_train(scheme, trains_above, shifts_above, next_train, next_shift + additional_shift)

    @staticmethod
    def trains_has_arrived(trains):
         if len(trains) == 0:
            return True

         has_arrived_list = list()
         for train in trains:
             has_arrived_list.append(train.has_arrived())
         return min(has_arrived_list)


def calculate_scheme_params(name):
    now = datetime.now()
    result_dict = dict()
    for rule_name, rule in rules_dict.items():
        print(rule_name)
        scheme = ConfigurationParser.load_configuration(name)

        ScheduleBuilder.make_schedule(scheme, rule)
        result_time = scheme.current_time - 1
        result_dict[rule_name] = result_time

    best_result = 999999
    best_rule = None
    worse_result = 0
    worse_rule = None
    sum = 0

    for key, value in result_dict.items():
        sum += value
        if value > worse_result:
            worse_result = value
            worse_rule = key
        if value < best_result:
            best_result = value
            best_rule = key

    print("time of calculation")
    print((datetime.now() - now).total_seconds())
    print("best")
    print(best_rule)
    print(best_result)
    print("worse")
    print(worse_rule)
    print(worse_result)
    print("avg")
    print(sum/len(result_dict))

calculate_scheme_params("sw30")


# for k in range(9):
#     n = 5 * (k+1)
# n = 15
# scheme = ConfigurationGenerator.create_random_scheme(n, n)
# ConfigurationParser.save_configuration(scheme, "sw" + str(n))
