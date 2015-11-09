# -*- coding: utf-8 -*-
class Station:

    name = None
    trains = None
    close_times = None

    def __init__(self, name, close_times=None):
        self.name = name
        if close_times is not None:
            self.close_times = close_times
        else:
            self.close_times = list()
        self.trains = set()

    def __repr__(self):
        return "Station\"%s\"" % str(self.name)

    def add_train(self, train):
        self.trains.add(train)