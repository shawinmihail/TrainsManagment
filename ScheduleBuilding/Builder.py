# -*- coding: utf-8 -*-
class Builder:

    MIN_TRAINS_DELAY = 1

    @staticmethod
    def create_scheme():
        import schemes
        return schemes.scheme1()

    @staticmethod
    def get_trains_data():
        data = list()
        data.append({"name": "2", "route": ["1", "3", "5"]})
        data.append({"name": "1", "route": ["1", "3", "1"]})
        data.append({"name": "3", "route": ["1", "3"]})
        data.append({"name": "4", "route": ["2", "3", "4"]})
        data.append({"name": "5", "route": ["2", "3"]})
        return data

    @staticmethod
    def set_trains_to_scheme(scheme, trains_data):
        trains = list()
        for train_info in trains_data:
            trains.append(scheme.add_train_by_route_names(train_info["name"], train_info["route"]))
        return trains

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
                        if abs(delay) < Builder.MIN_TRAINS_DELAY:
                            shift = Builder.MIN_TRAINS_DELAY - delay
                            return shift
        return None

    @staticmethod
    def simulate_train_adventure(scheme, train, shift, trains_above):
        scheme.current_time = 0
        train.relaunch(shift)
        while not train.has_arrived():
            scheme.update_trains_positions()

        # print(train.schedule)

        shift = Builder.find_shift(trains_above, train)
        return shift

    @staticmethod
    def make_schedule(scheme, rule):
        trains_above = list()
        trains_by_priority = rule(scheme.trains)
        for train in trains_by_priority:
            shift = 0
            while shift is not None:
                shift = Builder.simulate_train_adventure(scheme, train, shift, trains_above)
            trains_above.append(train)

        # for train in trains_by_priority:
        #     print(train.schedule)





scheme = Builder.create_scheme()
trains_data = Builder.get_trains_data()
Builder.set_trains_to_scheme(scheme, trains_data)

from ScheduleBuilding.Rules import *
Builder.make_schedule(scheme, name_rule)