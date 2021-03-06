# -*- coding: utf-8 -*-
from random import randint, uniform
from RailwayObjects.Way import Way
from RailwayObjects.Scheme import Scheme


class ConfigurationGenerator:

    STATIONS_PARAMS = {"suffix": "st", "close_times_amount": 0, "close_times_duration": 0, "close_time_gap": 0, "storage_price": 0}
    TRAINS_PARAMS = {"suffix": "tr", "route_len/stations_num": 0.3, "launch_cost": 0}
    WAYS_PARAMS = {"links_number": 2, "time_to_pass": 45, "one_direct_ratio": 0.1}
    ORDERS_PARAMS = {"linear_orders_number": 0, "amount": 0}

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
        links_number = ConfigurationGenerator.WAYS_PARAMS["links_number"]
        avg_time_to_pass = ConfigurationGenerator.WAYS_PARAMS["time_to_pass"]

        if ConfigurationGenerator.WAYS_PARAMS["one_direct_ratio"] != 0:
            ratio = int(1/ConfigurationGenerator.WAYS_PARAMS["one_direct_ratio"])
        else:
            ratio = 999999999

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
        avg_storage_price = ConfigurationGenerator.STATIONS_PARAMS["storage_price"]
        avg_launch_cost = ConfigurationGenerator.TRAINS_PARAMS["launch_cost"]
        for station in scheme.stations:
            price = uniform(avg_storage_price/2, avg_storage_price*2)
            station.set_storage_price(price)
        for train in scheme.trains:
            price = uniform(avg_launch_cost/2, avg_launch_cost*2)
            train.set_launch_cost(price)

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


class SimpleConfigurationGenerator:

    @staticmethod
    def add_brunch(scheme, suffix, length, attachment_st_name=None):
        from RailwayObjects.Way import Way
        last_st_name = None
        for n in range(length):
            st_name = suffix + str(n)
            scheme.add_station(st_name, set())
            if last_st_name is not None:
                scheme.add_way(randint(3, 12), st_name, last_st_name, Way.PROPERTY_TWO_DIRECT)
            else:
                if attachment_st_name is not None:
                    scheme.add_way(randint(3, 12), st_name, attachment_st_name, Way.PROPERTY_TWO_DIRECT)
            last_st_name = st_name

    @staticmethod
    def create_route_by_names_in_branch(suffix, ind1, ind2):
        names_list = list()
        for i in range(abs(ind2 - ind1)+ 1):
            if ind2 - ind1 > 0:
                names_list.append(suffix + str(ind1 + i))
            else:
                names_list.append(suffix + str(ind1 - i))
        return names_list

    @staticmethod
    def create_scheme232(number_of_trains, number_of_one_direct_ways):
        scheme = Scheme()

        SimpleConfigurationGenerator.add_brunch(scheme, "a", 71)
        SimpleConfigurationGenerator.add_brunch(scheme, "b", 41, "a10")
        SimpleConfigurationGenerator.add_brunch(scheme, "c", 36, "a20")
        SimpleConfigurationGenerator.add_brunch(scheme, "d", 51, "a40")
        SimpleConfigurationGenerator.add_brunch(scheme, "e", 33, "a60")

        a1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 40)
        a2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 20, 50)
        a3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 30, 70)


        b1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 0, 30)
        b2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 10, 20)
        b3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 15, 30)

        c1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 0, 15)
        c2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 0, 25)
        c3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 20, 25)

        d1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 25)
        d2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 20, 50)
        d3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 12)

        ab = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 10) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 0, 10)
        ac = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 20) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 0, 7)
        ad = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 40) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 15)
        ae = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 60) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("e", 0, 10)
        bad = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 10, 0) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 10, 40) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 5)


        route_list = [a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, ab, ac, ad, ae, bad]

        for i in range(number_of_trains):
            tr_name = "tr" + str(i)
            route = route_list[(i % len(route_list))]
            scheme.add_train(tr_name, route)

        for i in range(number_of_one_direct_ways):
            rand_index = randint(0, len(scheme.ways))
            k = 0
            for way in scheme.ways:
                if k == rand_index:
                    way.direct_property = Way.PROPERTY_ONE_DIRECT
                k += 1

        return scheme

    @staticmethod
    def create_scheme88(number_of_trains, number_of_one_direct_ways):
        scheme = Scheme()

        SimpleConfigurationGenerator.add_brunch(scheme, "a", 22)
        SimpleConfigurationGenerator.add_brunch(scheme, "b", 16, "a5")
        SimpleConfigurationGenerator.add_brunch(scheme, "c", 11, "a10")
        SimpleConfigurationGenerator.add_brunch(scheme, "d", 18, "a15")
        SimpleConfigurationGenerator.add_brunch(scheme, "e", 21, "a20")

        a1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 10)
        a2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 10, 20)
        a3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 7, 13)


        b1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 0, 7)
        b2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 0, 9)
        b3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 2, 8)

        c1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 2, 10)
        c2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 1, 5)
        c3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 8, 2)

        d1 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 6, 13)
        d2 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 17, 5)
        d3 = SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 8, 0)

        ab = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 5) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 0, 2)
        ac = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 10) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("c", 0, 7)
        ad = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 15) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 5)
        ae = SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 0, 20) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("e", 0, 10)
        bad = SimpleConfigurationGenerator.create_route_by_names_in_branch("b", 3, 0) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("a", 5, 15) + \
              SimpleConfigurationGenerator.create_route_by_names_in_branch("d", 0, 2)


        route_list = [a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, ab, ac, ad, ae, bad]

        for i in range(number_of_trains):
            tr_name = "tr" + str(i)
            route = route_list[(i % len(route_list))]
            scheme.add_train(tr_name, route)

        for i in range(number_of_one_direct_ways):
            rand_index = randint(0, len(scheme.ways))
            k = 0
            for way in scheme.ways:
                if k == rand_index:
                    way.direct_property = Way.PROPERTY_ONE_DIRECT
                k += 1

        return scheme

