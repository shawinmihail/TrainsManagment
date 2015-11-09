# -*- coding: utf-8 -*-
from RailwayObjects.Scheme import Scheme
from random import randint


class ConfigurationGenerator:

    @staticmethod
    def add_stations(scheme, number):
        st_header = "st"
        stations_names = list()
        closes_times = list()
        for n in range(number):
            stations_names.append(st_header + str(n))
            start_of_close_time = randint(0, 555)
            end_of_close_time = start_of_close_time + randint(0, 333)
            closes_times.append([[start_of_close_time, end_of_close_time]])
        scheme.add_stations_by_names(stations_names, closes_times)

    @staticmethod
    def add_ways_randomly(scheme):
        for station in scheme.stations:
            links_for_station = randint(2, 4)
            for n in range(links_for_station):
                time_to_pass = randint(15, 120)
                random_station = ConfigurationGenerator.find_random_station(scheme)
                while random_station == station:
                    random_station = ConfigurationGenerator.find_random_station(scheme)
                scheme.add_way(time_to_pass, station.name, random_station.name)

    @staticmethod
    def add_trains_randomly(scheme, number, avg_route_len):
        tr_header = "tr"
        for n in range(number):
            name = tr_header + str(n)
            length = randint(int(avg_route_len/2), int(avg_route_len * 2))
            station_names = ConfigurationGenerator.find_random_route_by_names(scheme, length)
            scheme.add_train_by_route_names(name, station_names)

    @staticmethod
    def find_random_route_by_names(scheme, length):
        stations_names = list()
        st1 = None
        for k in range(length):
            if k == 0:
                st1 = ConfigurationGenerator.find_random_station(scheme)
            possible_stations = ConfigurationGenerator.find_possible_to_move_stations(scheme, st1)
            st2 = possible_stations[randint(0, len(possible_stations) - 1)]
            stations_names.append(st1.name)
            st1 = st2
        return stations_names

    @staticmethod
    def find_possible_to_move_stations(scheme, station):
        possible_stations = list()
        for way in scheme.ways:
            if station in way.stations_on_ends:
                for possible_station in way.stations_on_ends:
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
    def create_random_scheme(n_stations, n_trains):
        scheme = Scheme()
        ConfigurationGenerator.add_stations(scheme, n_stations)
        ConfigurationGenerator.add_ways_randomly(scheme)
        ConfigurationGenerator.add_trains_randomly(scheme, n_trains, int(n_stations/2) + 2)
        return scheme