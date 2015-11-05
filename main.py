# -*- coding: utf-8 -*-
from RailwayObjects.Station import Station
from RailwayObjects.Scheme import Scheme
from RailwayObjects.Way import Way
from RailwayObjects.Train import Train, Route

stations = {Station("1"),
            Station("2"),
            Station("3"),
            Station("4"),
            Station("5"),
            }

ways = {Way({"1", "3"}, 1),
        Way({"2", "3"}, 1),
        Way({"4", "3"}, 1),
        Way({"5", "3"}, 1),
        }

scheme = Scheme(stations, ways)

scheme.add_train_into_station("1", "pobeda")
scheme.add_train_into_station("2", "poragenie")

st1 = scheme.find_station_by_name("1")
st2 = scheme.find_station_by_name("2")
st3 = scheme.find_station_by_name("3")
st4 = scheme.find_station_by_name("4")
st5 = scheme.find_station_by_name("5")

w13 = scheme.find_way_by_end_names("1", "3")
w23 = scheme.find_way_by_end_names("5", "3")
w43 = scheme.find_way_by_end_names("4", "3")
w53 = scheme.find_way_by_end_names("5", "3")

route1 = Route([w13, w53])
route2 = Route([w23, w43])

scheme.set_route_to_train("pobeda", route1)
scheme.set_route_to_train("poragenie", route2)