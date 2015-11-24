# -*- coding: utf-8 -*-
from random import randint, uniform

from RailwayObjects.Scheme import Scheme


class ConfigurationGenerator:

    STATIONS_PARAMS = {"suffix": "st", "close_times_amount": 1, "close_times_duration": 15, "close_time_gap": 30, "storage_cost": 1}
    TRAINS_PARAMS = {"suffix": "tr", "route_len/stations_num": 0.5, "launch_cost": 4000}
    WAYS_PARAMS = {"links_number": 5, "time_to_pass": 10, "one_direct_ratio": 0.1}
    ORDERS_PARAMS = {"linear_orders_number": 1, "amount": 0.2}

    @staticmethod
    def add_stations(scheme, number):
        st_suffix = ConfigurationGenerator.STATIONS_PARAMS["suffix"]
        close_times_amount = ConfigurationGenerator.STATIONS_PARAMS["close_times_amount"]
        close_times_duration = ConfigurationGenerator.STATIONS_PARAMS["close_times_duration"]
        close_time_gap = ConfigurationGenerator.STATIONS_PARAMS["close_time_gap"]
        stations_names = list()
        closes_times = list()
        for n in range(number):
            stations_names.append(st_suffix + str(n))
            last_close_time_ended = 0
            closes_times_set = set()
            for k in range(randint(0, close_times_amount*2)):
                start_of_close_time = last_close_time_ended + randint(int(close_time_gap/2), close_time_gap*2)
                end_of_close_time = start_of_close_time + randint(int(close_times_duration/2), close_times_duration*2)
                last_close_time_ended = end_of_close_time
                closes_times_set.add((start_of_close_time, end_of_close_time))
            closes_times.append(closes_times_set)
        for name, set1 in zip(stations_names, closes_times):
            scheme.add_station(name, set1)

    @staticmethod
    def add_ways_randomly(scheme):
        from RailwayObjects.Way import Way
        links_number = ConfigurationGenerator.WAYS_PARAMS["links_number"]
        avg_time_to_pass = ConfigurationGenerator.WAYS_PARAMS["time_to_pass"]
        ratio = int(1/ConfigurationGenerator.WAYS_PARAMS["one_direct_ratio"])
        one_direct_flag = 0
        for station in scheme.stations:
            for n in range(randint(1, links_number)):
                one_direct_flag += 1
                if divmod(one_direct_flag, ratio)[1] == 0:
                    property = Way.PROPERTY_ONE_DIRECT
                else:
                    property = Way.PROPERTY_TWO_DIRECT

                time_to_pass = randint(int(avg_time_to_pass/2), avg_time_to_pass*2)
                random_destination = ConfigurationGenerator.find_random_station(scheme)
                k = 0
                while random_destination == station:
                    k += 1
                    assert k < 999
                    random_destination = ConfigurationGenerator.find_random_station(scheme)
                scheme.add_way(time_to_pass, station.name, random_destination.name, property)

    @staticmethod
    def add_trains_randomly(scheme, number):
        tr_suffix = ConfigurationGenerator.TRAINS_PARAMS["suffix"]
        ratio = ConfigurationGenerator.TRAINS_PARAMS["route_len/stations_num"]
        stations_number = len(scheme.stations)
        for n in range(number):
            name = tr_suffix + str(n)
            length = randint(max(int(stations_number*ratio), 2), max(int(stations_number*ratio*2), 2))
            station_names = ConfigurationGenerator.find_random_route(scheme, length)
            scheme.add_train(name, station_names)

    @staticmethod
    def add_orders_randomly(scheme):
        for train in scheme.trains:
            own_index = -1
            for station in train.position.route:

                own_index += 1
                if own_index == len(train.position.route) - 1:
                    break

                linear_orders_number = ConfigurationGenerator.ORDERS_PARAMS["linear_orders_number"]
                amount = ConfigurationGenerator.ORDERS_PARAMS["amount"]

                for k in range(randint(0, int(linear_orders_number * 2))):
                    new_amount = uniform(amount / 2, amount * 2)

                    destination_name = None
                    k = 0
                    while True:
                        k += 1
                        assert k < 999
                        index = randint(own_index + 1, len(train.position.route) - 1)
                        destination_name = train.position.route[index].name
                        if destination_name != station.name:
                            break

                    station.add_linear_order(new_amount, destination_name, train.name)

    @staticmethod
    def add_storage_and_launch_costs_randomly(scheme):
        avg_storage_cost = ConfigurationGenerator.STATIONS_PARAMS["storage_cost"]
        avg_launch_cost = ConfigurationGenerator.TRAINS_PARAMS["launch_cost"]
        for station in scheme.stations:
            cost = uniform(avg_storage_cost/2, avg_storage_cost*2)
            station.set_storage_cost(cost)
        for train in scheme.trains:
            cost = uniform(avg_launch_cost/2, avg_launch_cost*2)
            train.set_launch_cost(cost)

    @staticmethod
    def find_random_route(scheme, length):
        stations_names = list()
        st1 = None
        for k in range(length):
            if k == 0:
                st1 = ConfigurationGenerator.find_random_station(scheme)
            possible_stations = ConfigurationGenerator.find_possible_to_move_stations(scheme, st1)

            for n in range(15):
                st2 = possible_stations[randint(0, len(possible_stations) - 1)]
                if st2.name not in stations_names:
                    break

            stations_names.append(st1.name)
            st1 = st2
        return stations_names

    @staticmethod
    def find_possible_to_move_stations(scheme, station):
        possible_stations = list()
        for way in scheme.ways:
            if station in way.stations:
                for possible_station in way.stations:
                    if possible_station != station:
                        possible_stations.append(possible_station)

        assert len(possible_stations) != 0
        return possible_stations

    @staticmethod
    def find_random_station(scheme):
        random_station_number = randint(0, len(scheme.stations) - 1)
        k = 0
        for station in scheme.stations:
            if k == random_station_number:
                return station
            k += 1
        assert False

    @staticmethod
    def create_random_scheme(n_stations, n_trains, do_orders=True, do_costs=True):
        scheme = Scheme()
        ConfigurationGenerator.add_stations(scheme, n_stations)
        ConfigurationGenerator.add_ways_randomly(scheme)
        ConfigurationGenerator.add_trains_randomly(scheme, n_trains)
        if do_orders:
            ConfigurationGenerator.add_orders_randomly(scheme)
        if do_costs:
            ConfigurationGenerator.add_storage_and_launch_costs_randomly(scheme)
        return scheme