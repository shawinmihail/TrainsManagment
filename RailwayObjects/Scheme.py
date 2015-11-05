# -*- coding: utf-8 -*-
from RailwayObjects.Train import Train


class Scheme:

    stations = None
    ways = None
    trains = None

    def __init__(self, stations, ways):
        self.stations = stations
        self.ways = ways
        self.trains = set()

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
            raise Exception("same names!")
        if len(self.ways) == 0:
            raise Exception("No ways at all!")
        for way in self.ways:
            pair = way.stations_on_ends
            if station_name1 in pair and station_name_2 in pair:
                return way
        return None

    # def verify_route(self, route):
    #     for station1, station2 in zip(route.stations, route.stations[1:]):
    #         result = self.find_way_by_end_names(station1.name, station2.name)
    #         if result:
    #             return True
    #         else:
    #             return False

    def verify_route(self, route):
        for way in route.ways:
            if way in self.ways:
                return True
            else:
                return False

    def add_train_into_station(self, station_name, train_name):
        dispatch = self.find_station_by_name(station_name)
        if dispatch:
            train = Train(train_name, dispatch)
            dispatch.add_train(train)
            self.trains.add(train)
        else:
            raise Exception("No such station!")

    def set_route_to_train(self, train_name, route):
        train = self.find_train_by_name(train_name)
        route_is_valid = self.verify_route(route)
        if not route_is_valid:
            raise Exception("Route is not valid!")
        if train:
            train.set_route(route)
        else:
            raise Exception("No such train!")

    def upgrade_trains_positions(self):
        if len(self.trains) == 0:
            raise Exception("no trains at all!")
        for train in self.trains:
            pass
