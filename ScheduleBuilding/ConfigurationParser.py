# -*- coding: utf-8 -*-
from RailwayObjects.Scheme import Scheme


class ConfigurationParser:

    PATH = "../configurations/"

    @staticmethod
    def save_configuration(scheme, name):
        path = ConfigurationParser.PATH + name
        conf_file = open(path, "w")

        conf_file.write("stations\n")
        station_str = ""
        for station in scheme.stations:
            station_str += station.name + "-" + str(station.close_times[0][0]) + "," + str(station.close_times[0][1]) + ";"
        conf_file.write(station_str[:-1])
        conf_file.write("\n")

        conf_file.write("ways\n")
        ways_str = ""
        for way in scheme.ways:
            ways_str += str(way.time_to_pass) + "," + \
                        str(way.stations_on_ends_names())[1:-1].replace(" ", "").replace("'", "") + ";"
        conf_file.write(ways_str[:-1])
        conf_file.write("\n")

        conf_file.write("trains\n")
        trains_str = ""
        for train in scheme.trains:
            route_str = ""
            trains_str += train.name + "-"
            for station in train.route:
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
        stations_info = stations_line.split(";")

        conf_file.readline()
        ways_line = conf_file.readline().rstrip()
        ways_info = ways_line.split(";")

        conf_file.readline()
        trains_line = conf_file.readline().rstrip()
        trains_info = trains_line.split(";")

        # stations_names = list()
        # times = list()
        # for station_info in stations_info:
            # name, closes_times = station_info.split("-")
            # name = station_info.split("-")
            # t1, t2 = closes_times.split(",")
            # stations_names.append(name)
            # times.append([[int(t1), int(t2)]])
        scheme.add_stations_by_names(stations_info)

        for way_info in ways_info:
            time, st1, st2 = way_info.split(",")
            scheme.add_way(int(time), st1, st2)
        for train_info in trains_info:
            name, stations_names = ConfigurationParser.parse_trains_info(train_info)
            scheme.add_train_by_route_names(name, stations_names)

        return scheme

    @staticmethod
    def parse_trains_info(train_info):
        name, stations_names_string = train_info.split("-")
        station_names = stations_names_string.split(",")
        return name, station_names