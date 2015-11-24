# -*- coding: utf-8 -*-
from RailwayObjects.Scheme import Scheme


class ConfigurationParser:

    PATH = "../configurations/"

    @staticmethod
    def save_configuration(scheme, name):
        path = ConfigurationParser.PATH + name
        conf_file = open(path, "w")

        conf_file.write("stations\n")
        stations_str = ""
        for station in scheme.stations:
            closes_times_str = ""
            for close_time in station.close_times:
                close_time_str = "[%s,%s]," % (close_time[0], close_time[1])
                closes_times_str += close_time_str
            station_info_str = "%s-%s;" % (station.name, closes_times_str[:-1])
            stations_str += station_info_str
        conf_file.write(stations_str[:-1])
        conf_file.write("\n")

        conf_file.write("ways\n")
        ways_str = ""
        for way in scheme.ways:
            ways_str += "%s,%s-%s-%s;"\
                        % (way.stations[0].name, way.stations[1].name, way.time_to_pass, way.direct_property)
        conf_file.write(ways_str[:-1])
        conf_file.write("\n")

        conf_file.write("trains\n")
        trains_str = ""
        for train in scheme.trains:
            route_str = ""
            trains_str += train.name + "-"
            for station in train.position.route:
                route_str += station.name + ","
            trains_str += route_str[:-1] + ";"
        conf_file.write(trains_str[:-1])

        conf_file.close()

    @staticmethod
    def load_configuration(name):

        path = ConfigurationParser.PATH + name

        scheme = Scheme()
        conf_file = open(path, "r")
        conf_file.readline()
        stations_line = conf_file.readline().rstrip()
        names, times_sets = ConfigurationParser.parse_stations_string(stations_line)
        for name, time_set in zip(names, times_sets):
            scheme.add_station(name, time_set)

        conf_file.readline()
        ways_line = conf_file.readline().rstrip()
        times_to_pass, st1_names, st2_names, direct_properties = ConfigurationParser.parse_ways_string(ways_line)
        for time, st1, st2, property in zip(times_to_pass, st1_names, st2_names, direct_properties):
            scheme.add_way(time, st1, st2, property)

        conf_file.readline()
        trains_line = conf_file.readline().rstrip()
        names, routes = ConfigurationParser.parse_trains_string(trains_line)
        for name, route in zip(names, routes):
            scheme.add_train(name, route)

        return scheme

    @staticmethod
    def parse_stations_string(stations_string):
        names = list()
        times_sets = list()
        stations_info = stations_string.split(";")
        for one_station_info in stations_info:
            name, times_info = one_station_info.split("-")
            times_set = ConfigurationParser.parse_times_info(times_info)
            names.append(name)
            times_sets.append(times_set)
        return names, times_sets

    @staticmethod
    def parse_ways_string(ways_string):
        times_to_pass = list()
        st1_names = list()
        st2_names = list()
        direct_properties = list()
        ways_info = ways_string.split(";")
        for one_way_info in ways_info:
            st1_st2, time_to_pass, property = one_way_info.split("-")
            st1, st2 = st1_st2.split(",")
            times_to_pass.append(int(time_to_pass))
            st1_names.append(st1)
            st2_names.append(st2)
            direct_properties.append(property)

        return times_to_pass, st1_names, st2_names, direct_properties

    @staticmethod
    def parse_trains_string(trains_string):
        names = list()
        routes = list()
        trains_info = trains_string.split(";")
        for one_train_info in trains_info:
            name, route_info = one_train_info.split("-")
            station_names = route_info.split(",")
            names.append(name)
            routes.append([station_name for station_name in station_names])

        return names, routes

    @staticmethod
    def parse_times_info(times_info):
        times_set = set()
        times_info = times_info.replace("]", "").replace("[", "")
        start_times_in_order = times_info.split(",")[::2]
        end_times_in_order = times_info.split(",")[1::2]
        for start_time, end_time in zip(start_times_in_order, end_times_in_order):
            times_set.add((int(start_time), int(end_time)))
        return times_set