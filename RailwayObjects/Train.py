# -*- coding: utf-8 -*-
from copy import copy
from RailwayObjects.Station import Load


class Train:

    name = None
    position = None
    schedule = None
    loads = None
    launch_cost = None
    ready_time = None

    def __init__(self, name, route, ways):
        self.name = name
        self.position = Position(route, ways)
        self.schedule = list()
        self.loads = set()
        self.ready_time = 0

    def __repr__(self):
        dispatch = self.position.route[self.position.dispatch_index]
        time_in_way = self.position.time_in_way
        destination = self.position.destination()
        # return "Train: %s, Status: %s, dispatch %s, destination %s, time in way %s" % \
        #     (self.name, self.position.status, dispatch, destination, time_in_way)
        return self.name

    def set_launch_cost(self, launch_cost):
        self.launch_cost = launch_cost

    def launch(self):
        self.position.status = Position.STATUS_MOVING

    def is_ready(self, t):
        if t < self.ready_time:
            return False
        else:
            return True

    def reset(self):
        self.schedule = list()
        self.position.reset()
        self.position.status = Position.STATUS_WAITING

    def update_position(self, current_time):
        if not self.is_ready(current_time):
            return

        self.define_status()
        self.record_schedule(current_time)

        if self.position.time_in_way == 0:
                self.exchange_loads(self.position.dispatch())

        if self.position.status == Position.STATUS_MOVING:

            time_to_pass = self.position.way().time_to_pass
            was_passed = self.position.time_in_way

            if time_to_pass > was_passed + 1:
                self.position.time_in_way += 1
                return
            else:
                self.position.dispatch_index += 1
                self.position.define_destination_index()
                self.position.time_in_way = 0

    def exchange_loads(self, station):
        self.take_loads(station)
        self.put_loads(station)

    def take_loads(self, station):
        for load in station.loads:
            if load.train_name == self.name:
                self.add_load(load)
                station.remove_load(load)

    def put_loads(self, station):
        for load in self.loads:
            if load.destination_station_name == station.name:
                station.add_load(load)
                self.remove_load(load)

    def add_load(self, load, amount=None):
        if amount is None:
            amount = load.amount
        for own_load in self.loads:
            if load.destination_station_name == own_load.destination_station_name\
            and load.train_name == own_load.train_name:
                    own_load.add(amount)
                    return
        load = Load(amount, load.destination_station_name, load.train_name)
        self.loads.add(load)

    def remove_load(self, load, amount=None):
        if amount is None:
            amount = load.amount
        for own_load in self.loads:
            if load.destination_station_name == own_load.destination_station_name\
            and load.train_name == own_load.train_name:
                    own_load.remove(amount)
                    return
        assert False

    def record_schedule(self, current_time):
        self.position.time = current_time
        self.schedule.append(copy(self.position))

    def define_status(self):
        if self.position.status == Position.STATUS_WAITING:
            self.position.status = Position.STATUS_WAITING
        elif self.position.status == Position.STATUS_ARRIVED:
            self.position.status = Position.STATUS_ARRIVED
        elif self.position.status == Position.STATUS_MOVING:
            self.position.status = Position.STATUS_MOVING
            destination_index = self.position.define_destination_index()
            if destination_index is None:
                self.status = Position.STATUS_ARRIVED
                self.position.status = Position.STATUS_ARRIVED

    def has_arrived(self):
        if self.position.status == Position.STATUS_ARRIVED:
            return True
        else:
            return False

    def ways_time_sum(self):
        sum1 = 0
        for way in self.position.ways:
            sum1 += way.time_to_pass
        return sum1


class Position:

    dispatch_index = None
    destination_index = None
    time_in_way = None
    time = 0
    route = None
    ways = None
    status = None

    STATUS_MOVING = "moving"
    STATUS_WAITING = "waiting"
    STATUS_ARRIVED = "arrived"

    def __init__(self, route, ways, dispatch_index=0, time_in_current_way=0):
        assert len(route) >= 2
        assert len(ways) >= 1
        self.dispatch_index = dispatch_index
        self.destination_index = dispatch_index + 1
        self.time_in_way = time_in_current_way
        self.route = route
        self.ways = ways
        self.status = Position.STATUS_WAITING

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
        if self.destination_index is not None:
            return self.route[self.destination_index]
        else:
            return None

    def way(self):
        assert self.destination_index != self.dispatch_index
        if self.destination_index is None:
            return None
        dispatch = self.dispatch()
        destination = self.destination()
        for way in self.ways:
            if dispatch in way.stations and destination in way.stations:
                return way
        raise Exception("go to wrong way!")

    def define_destination_index(self):
        max_index = len(self.route) - 1
        if max_index == self.dispatch_index:
            self.destination_index = None
        else:
           self.destination_index = self.dispatch_index + 1

        return self.destination_index

    def route_by_names(self):
        route_by_names = list()
        for st in self.route:
            route_by_names.append(st.name)
        return route_by_names

    def find_remaining_time_to_current_destination(self):
        if self.way() is None:
            return None
        return self.way().time_to_pass - self.time_in_way

    def reset(self):
        self.dispatch_index = 0
        self.destination_index = 1
        self.time_in_way = 0
        self.time = 0