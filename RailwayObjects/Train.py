# -*- coding: utf-8 -*-
from copy import copy


class Train:

    name = None
    route = None
    ways = None
    position = None
    schedule = None

    def __init__(self, name, route, ways):
        if len(route) < 2:
            raise Exception("incorrect route!")
        if len(ways) < 1:
            raise Exception("incorrect ways!")

        dispatch_index = 0
        self.name = name
        self.route = route
        self.ways = ways
        self.position = Position(dispatch_index, 0, route, ways)
        self.schedule = list()

    def __repr__(self):
        dispatch = self.route[self.position.dispatch_index]
        destination_index = self.position.destination_index
        time_in_way = self.position.time_in_way
        if destination_index:
            destination = self.route[self.position.destination_index]
            return "Train: %s, move from %s to %s for time %s" % \
               (self.name, dispatch, destination, time_in_way)
        else:
            return "Train: %s, wait on %s" % \
               (self.name, dispatch)

    def launch(self):
        self.find_current_destination_index()

    def reset(self):
        self.schedule = list()
        self.position.reset()

    def record_schedule(self, current_time):
        self.position.time = current_time
        self.schedule.append(copy(self.position))

    def update_position(self, dt, current_time):
        self.record_schedule(current_time)

        current_way = self.position.way()
        if current_way is None:
            return

        time_to_pass = self.position.way().time_to_pass
        was_passed = self.position.time_in_way

        if time_to_pass > was_passed + dt:
            self.position.time_in_way += dt
            return
        else:
            self.position.dispatch_index += 1
            self.find_current_destination_index()
            self.position.time_in_way = 0
            dt -= time_to_pass - was_passed
            return self.update_position(dt, current_time)

    def find_current_destination_index(self):
        dispatch_index = self.position.dispatch_index
        max_index = len(self.route) - 1
        if max_index == dispatch_index:
            self.position.destination_index = None
        else:
           self.position.destination_index = dispatch_index + 1

    def has_arrived(self):
        if self.position.dispatch_index == len(self.route) - 1:
            return True
        else:
            return False


class Position:

    dispatch_index = None
    destination_index = None
    time_in_way = None
    time = 0
    route = None
    ways = None

    def __init__(self, dispatch_index, time_in_current_way, route, ways):
        self.dispatch_index = dispatch_index
        self.time_in_way = time_in_current_way
        self.route = route
        self.ways = ways

    def __repr__(self):
        if self.destination_index is None:
            return "[%s] (%s)"\
               % (self.time, self.dispatch())
        else:
            return "[%s] (%s -> %s, %s)"\
               % (self.time, self.dispatch(), self.destination(), self.time_in_way)

    def dispatch(self):
        return self.route[self.dispatch_index]

    def destination(self):
        return self.route[self.destination_index]

    def way(self):
        if self.dispatch_index == self.destination_index:
            raise Exception("same destination and dispatch")
        if self.destination_index is None:
            return None
        dispatch = self.dispatch()
        destination = self.destination()
        for way in self.ways:
            if dispatch in way.stations_on_ends and destination in way.stations_on_ends:
                return way
        raise Exception("go to wrong way!")

    def reset(self):
        self.dispatch_index = 0
        self.destination_index = None
        self.time_in_way = 0
        self.time = 0