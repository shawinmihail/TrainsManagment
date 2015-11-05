# -*- coding: utf-8 -*-
class Train:

    name = None
    position = None
    route = None

    def __init__(self, name, dispatch):
        self.position = Position(dispatch, destination=None, time_in_way=0)
        self.name = name

    def set_route(self, route):
        self.route = route



    def upgrade_position(self):
        pass

    # def find_destination(self):
    #     if self.route:



class Position:

    dispatch = None
    destination = None
    time_in_way = None

    def __init__(self, dispatch, destination, time_in_way):
        self.dispatch = dispatch
        self.destination = destination
        self.time_in_way = time_in_way


class Route:

    ways = None
    stations = None

    def __init__(self, stations, ways):
        self.stations = stations