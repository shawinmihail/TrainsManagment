# -*- coding: utf-8 -*-
from RailwayObjects.Station import Station
from RailwayObjects.Scheme import Scheme


def scheme1():
    stations = {Station("1"),
                Station("2"),
                Station("3"),
                Station("4"),
                Station("5"),
                }

    scheme = Scheme(stations)
    scheme.set_way(11, "1", "3")
    scheme.set_way(12, "2", "3")
    scheme.set_way(13, "4", "3")
    scheme.set_way(14, "5", "3")

    # scheme.add_train_by_route_names("pobeda", ["1", "3", "5"])
    # scheme.add_train_by_route_names("lenin", ["2", "3", "4"])

    # st1 = scheme.find_station_by_name("1")
    # st2 = scheme.find_station_by_name("2")
    # st3 = scheme.find_station_by_name("3")
    # st4 = scheme.find_station_by_name("4")
    # st5 = scheme.find_station_by_name("5")
    #
    # w13 = scheme.find_way_by_end_names("1", "3")
    # w23 = scheme.find_way_by_end_names("5", "3")
    # w43 = scheme.find_way_by_end_names("4", "3")
    # w53 = scheme.find_way_by_end_names("5", "3")

    # t1 = scheme.find_train_by_name("pobeda")
    # t2 = scheme.find_train_by_name("lenin")

    return scheme