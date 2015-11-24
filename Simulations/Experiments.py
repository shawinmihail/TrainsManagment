# -*- coding: utf-8 -*-
from Simulations.Rules import *
from Gui.GantDiagrammCreator import *
from Simulations.ConfigurationParser import ConfigurationParser
from Simulations.ConfigurationGenerator import ConfigurationGenerator
from Simulations.ScheduleViewer import ScheduleViewer
from datetime import datetime
import math


class ScheduleBuilder:

    MIN_TRAINS_DELAY = 5

    @staticmethod
    def find_shift(trains_above, train):
        own_schedule = train.schedule

        for t in range(len(own_schedule)):
            own_position = own_schedule[t]
            own_status = own_position.status
            own_way = own_position.way()
            if own_status == own_position.STATUS_WAITING or own_status == own_position.STATUS_ARRIVED:
                continue
            windows_conflict_shift = ScheduleBuilder.check_window_conflicts(own_position)
            if windows_conflict_shift > 0:
                return windows_conflict_shift

            for other_train in trains_above:
                other_schedule = other_train.schedule
                other_position = other_schedule[t]
                other_way = other_position.way()
                if own_way == other_way:
                    assert own_way is not None
                    if own_way.direct_property == own_way.PROPERTY_TWO_DIRECT:
                        trains_conflict_shift = \
                            ScheduleBuilder.check_trains_conflict_on_two_direct_way(own_position, other_position)
                    elif own_way.direct_property == own_way.PROPERTY_ONE_DIRECT:
                        trains_conflict_shift = \
                            ScheduleBuilder.check_trains_conflict_on_one_direct_way(own_position, other_position)
                    else:
                        assert False
                    if trains_conflict_shift > 0:
                        return trains_conflict_shift

        return None

    @staticmethod
    def check_trains_conflict_on_two_direct_way(own_position, other_position):
        own_dispatch = own_position.dispatch()
        other_dispatch = other_position.dispatch()
        if own_dispatch == other_dispatch:
            own_time_in_way = own_position.time_in_way
            other_time_in_way = other_position.time_in_way
            delay = own_time_in_way - other_time_in_way
            if abs(delay) < ScheduleBuilder.MIN_TRAINS_DELAY:
                shift = ScheduleBuilder.MIN_TRAINS_DELAY - delay
                return shift
        return -1

    @staticmethod
    def check_trains_conflict_on_one_direct_way(own_position, other_position):
        own_dispatch = own_position.dispatch()
        other_dispatch = other_position.dispatch()
        if own_dispatch == other_dispatch:
            return ScheduleBuilder.check_trains_conflict_on_two_direct_way(own_position, other_position)
        else:
            return other_position.find_remaining_time_to_current_destination()

    @staticmethod
    def check_window_conflicts(own_position):
        own_dispatch = own_position.dispatch()
        for close_time in own_dispatch.close_times:
            arrival_time = own_position.time + own_position.find_remaining_time_to_current_destination()
            if close_time[0] < arrival_time < close_time[1]:
                shift = arrival_time - close_time[0]
                return shift
        return -1

    @staticmethod
    def make_schedule(scheme, rule):
        trains_above = list()
        trains_by_priority = rule(scheme.trains)
        shifts_above = list()
        for train in trains_by_priority:
            shift = ScheduleBuilder.simulate_train(scheme, trains_above, shifts_above, train, 0)
            shifts_above.append(shift)
            trains_above.append(train)
            print("")
            print("trains_was_calculated - ")
            print(len(trains_above))

        # for train in trains_by_priority:
        #     print(train.schedule)

    @staticmethod
    def simulate_train(scheme, trains_above, shifts_above, train, shift):
        scheme.reset()
        # simulate trains above
        while not ScheduleBuilder.trains_has_arrived(trains_above + [train]):
            t = scheme.current_time

            # launch trains above with calculated shift
            for train_above, shift_above in zip(trains_above, shifts_above):
                if t >= shift_above:
                    train_above.launch()

            # launch next train
            if t >= shift:
                train.launch()
            scheme.tick()

        # sum shift while there not will be conflicts
        additional_shift = ScheduleBuilder.find_shift(trains_above, train)
        if additional_shift is None:
            return shift
        else:
            return ScheduleBuilder.simulate_train(scheme, trains_above, shifts_above, train, shift + additional_shift)

    @staticmethod
    def trains_has_arrived(trains):
         if len(trains) == 0:
            return True

         has_arrived_list = list()
         for train in trains:
             has_arrived_list.append(train.has_arrived())
         return min(has_arrived_list)

    @staticmethod
    def calculate_scheme_params(name):
        now = datetime.now()
        result_dict = dict()

        for rule_name, rule in rules_dict.items():

            if rule_name != "random1_rule":
                continue

            print(rule_name)
            scheme = ConfigurationParser.load_configuration(name)

            ScheduleBuilder.make_schedule(scheme, rule)
            result_time = scheme.current_time - 1
            result_dict[rule_name] = result_time

        best_result = 999999999
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

        # calculate at the end with the best rule
        # scheme = ConfigurationParser.load_configuration(name)
        # ScheduleBuilder.make_schedule(scheme, rules_dict[best_rule])

        print("")
        print("time of calculation")
        print((datetime.now() - now).total_seconds())
        print("best")
        print(best_rule)
        print(best_result)
        print("avg")
        print(sum/len(result_dict))
        print("worse")
        print(worse_rule)
        print(worse_result)
        print("one_direct_ways")
        print(scheme.number_of_one_directed_ways())
        print("two_direct_ways")
        print(scheme.number_of_two_directed_ways())


class PeriodsCalculator:

    # @staticmethod
    # def generate_trains_set(scheme, finish_time):
    #     trains_list = list()
    #     period_dict = PeriodsCalculator.create_period_dict(scheme)
    #     for t in range(finish_time):
    #         for train_name, period in period_dict:
    #             if t % period == 0 and t != 0:
    #                 train = scheme.add_train(train_name)
    #                 trains_list.append()

    @staticmethod
    def create_period_dict(scheme):
        period_dict = dict()
        for train in scheme.trains:
            period = PeriodsCalculator.calculate_period_for_train(train)
            assert period > 0
            period_dict[train.name] = period
        return period_dict

    @staticmethod
    def calculate_period_for_train(train):
        denominator = 0
        for station in train.position.route:
            denominator += sum([order.coeff for order in station.orders]) * station.storage_cost
        period = math.sqrt(2*train.launch_cost / denominator)
        return int(period)


def delivery_test():

    scheme = ConfigurationGenerator.create_random_scheme(25, 10)
    first_train = scheme.find_train_by_name("tr0")
    first_train.launch()
    first_station = first_train.position.dispatch()
    print(first_station.orders)

    ITERATIONS = 50
    PERIOD = 10

    for t in range(ITERATIONS):
        if t % PERIOD == 0 and t != 0:
            name = "tr0"
            route_by_names = first_train.position.route_by_names()
            new_train = scheme.add_train(name, route_by_names)
            new_train.launch()

        scheme.tick()
        print(first_station.loads)
        # print(first_train)


def simple_delivery_test():

    scheme = ConfigurationGenerator.create_random_scheme(2, 0)
    st0 = scheme.find_station_by_name("st0")
    st1 = scheme.find_station_by_name("st1")
    st0.add_linear_order(1, "st1", "tr0")
    tr0 = None

    ITERATIONS = 30
    PERIOD = 10

    for t in range(ITERATIONS):

        if t == 3:
            tr0 = scheme.add_train("tr0", ["st0", "st1"])
            tr0.launch()

        print(t)
        try:
            print(tr0.loads)
            print(tr0.position)
        except:
            pass
        # print(st0.loads)

        scheme.tick()

scheme = ConfigurationGenerator.create_random_scheme(25, 10)
print(PeriodsCalculator.create_period_dict(scheme))


