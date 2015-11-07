# -*- coding: utf-8 -*-
from RailwayObjects.Train import Train
from RailwayObjects.Way import Way


class Scheme:

    stations = None
    ways = None
    trains = None
    current_time = 0

    def __init__(self, stations):
        self.stations = stations
        self.ways = set()
        self.trains = set()

    def set_way(self, time_to_pass, st_name1, st_name2):
        st1 = self.find_station_by_name(st_name1)
        st2 = self.find_station_by_name(st_name2)
        if st1 is None or st2 is None:
            raise Exception("No such stations")
        way = Way(st1, st2, time_to_pass)
        self.ways.add(way)

    def find_station_by_name(self, station_name):
        if len(self.stations) == 0:
            raise Exception("No stations at all!")
        for station in self.stations:
            if station_name == station.name:
                return station
        return None

    def find_train_by_name(self, train_name):
        if len(self.trains) == 0:
            raise Exception("No trains at all!")
        for train in self.trains:
            if train_name == train.name:
                return train
        return None

    def find_way_by_end_names(self, station_name1, station_name_2):
        if station_name1 == station_name_2:
            raise Exception("no way to same station!")
        if len(self.ways) == 0:
            raise Exception("No ways at all!")
        for way in self.ways:
            st_names_on_ends = way.stations_on_ends_names()
            if station_name1 in st_names_on_ends and station_name_2 in st_names_on_ends:
                return way
        return None

    def find_route_by_stations_names(self, stations_names):
        route = list()
        for station_name in stations_names:
            station = self.find_station_by_name(station_name)
            if station is None:
                raise Exception("No such station!")
            route.append(station)
        return route

    def add_train_by_route_names(self, train_name, route_by_names):
        dispatch_name = route_by_names[0]
        dispatch = self.find_station_by_name(dispatch_name)
        if dispatch is None:
            raise Exception("No such station")

        route = self.find_route_by_stations_names(route_by_names)
        ways = self.find_ways_of_route(route)
        train = Train(train_name, route, ways)
        self.trains.add(train)
        dispatch.add_train(train)
        return train

    def find_ways_of_route(self, route):
        ways = list()
        for station1, station2 in zip(route, route[1:]):
            way = self.find_way_by_end_names(station1.name, station2.name)
            if way is None:
                raise Exception("No way for the route")
            ways.append(way)
        return ways

    def tick(self, dt=1):
        if len(self.trains) == 0:
            raise Exception("no trains at all!")
        for train in self.trains:
            train.update_position(dt, self.current_time)
        self.current_time += dt

    def reset(self):
        self.current_time = 0
        if len(self.trains) == 0:
            raise Exception("no trains at all!")
        for train in self.trains:
            train.reset()

    def all_trains_has_arrived(self):
        if len(self.trains) == 0:
            raise Exception("no trains at all!")
        has_arrived_list = list()
        for train in self.trains:
            has_arrived_list.append(train.has_arrived())
        return min(has_arrived_list)