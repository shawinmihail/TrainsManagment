# -*- coding: utf-8 -*-
class Station:

    name = None
    trains = None
    close_times = None
    orders = None
    loads = None
    storage_price = None
    storage_costs = None

    def __init__(self, name, close_times):
        self.name = name
        self.close_times = close_times
        self.trains = set()
        self.orders = set()
        self.loads = set()
        self.storage_costs = 0

    def __repr__(self):
        return "Station\"%s\"" % str(self.name)

    def set_storage_price(self, cost):
        self.storage_price = cost

    def add_linear_order(self, coeff, dest_st_name, train_name):
        order = LinearOrder(coeff, dest_st_name, train_name)
        for existing_order in self.orders:
            if existing_order.destination_station_name == dest_st_name\
            and existing_order.train_name == train_name:
                existing_order.coeff += coeff
                return

        self.orders.add(order)

    def add_ordered_loads(self):
        for order in self.orders:
            load = Load(order.coeff, order.destination_station_name, order.train_name)
            self.add_load(load)

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

    def total_loads(self):
        return sum([load.amount for load in self.loads])

    def calculate_storage_costs(self):
        self.storage_costs += self.storage_price * self.total_loads()


class LinearOrder:

    coeff = None
    destination_station_name = None
    train_name = None

    def __init__(self, coeff, destination_station_name, train_name):
        self.coeff = coeff
        self.destination_station_name = destination_station_name
        self.train_name = train_name

    def __repr__(self):
        return "LinearOrder coeff %s, to %s, by %s" % (self.coeff, self.destination_station_name, self.train_name)


class Load:

    amount = None
    destination_station_name = None
    train_name = None

    def __init__(self, amount, destination_station_name, train_name):
        self.amount = amount
        self.destination_station_name = destination_station_name
        self.train_name = train_name

    def __repr__(self):
        return "Load %s to %s by %s" % (self.amount, self.destination_station_name, self.train_name)

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount
        assert self.amount >= 0