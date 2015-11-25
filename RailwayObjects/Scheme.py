# -*- coding: utf-8 -*-
from RailwayObjects.Train import Train
from RailwayObjects.Way import Way
from RailwayObjects.Station import Station


class Scheme:

    stations = None
    ways = None
    trains = None
    current_time = 0

    def __init__(self):
        self.stations = set()
        self.ways = set()
        self.trains = set()

    def add_station(self, name, closes_times_set):
        station = Station(name, closes_times_set)
        self.stations.add(station)

    def add_way(self, time_to_pass, st_name1, st_name2, direction_property):
        st1 = self.find_station_by_name(st_name1)
        st2 = self.find_station_by_name(st_name2)
        if st1 is None or st2 is None:
            raise Exception("No such stations")
        way = Way(st1, st2, time_to_pass, direction_property)
        if self.way_is_ok(way):
            self.ways.add(way)

    def way_is_ok(self, way):
        for existing_way in self.ways:
            if way.stations == existing_way.stations:
                return False
        return True

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

    def add_train(self, train_name, route_by_names):
        dispatch_name = route_by_names[0]
        dispatch = self.find_station_by_name(dispatch_name)
        if dispatch is None:
            raise Exception("No such station")

        route = self.find_route_by_stations_names(route_by_names)
        ways = self.find_ways_of_route(route)
        train = Train(train_name, route, ways)
        self.trains.add(train)
        return train

    def find_ways_of_route(self, route):
        ways = list()
        for station1, station2 in zip(route, route[1:]):
            way = self.find_way_by_end_names(station1.name, station2.name)
            if way is None:
                raise Exception("No way for the route")
            ways.append(way)
        return ways

    def tick(self):
        # assert len(self.trains) > 0
        assert len(self.stations) > 0
        self.current_time += 1
        for station in self.stations:
            station.add_ordered_loads()
        for train in self.trains:
            train.update_position(self.current_time)
        self.calculate_storage_costs_on_each_station()

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

    def number_of_one_directed_ways(self):
        assert len(self.ways) > 0
        res = 0
        for way in self.ways:
            if way.direct_property == Way.PROPERTY_ONE_DIRECT:
                res += 1
        return res

    def number_of_two_directed_ways(self):
        assert len(self.ways) > 0
        res = 0
        for way in self.ways:
            if way.direct_property == Way.PROPERTY_TWO_DIRECT:
                res += 1
        return res

    def calculate_storage_costs_on_each_station(self):
        assert len(self.stations) > 0
        for station in self.stations:
            station.calculate_storage_costs()
