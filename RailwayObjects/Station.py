# -*- coding: utf-8 -*-
class Station:

    name = None
    trains = None

    def __init__(self, name):
        self.name = name
        self.trains = set()

    def add_train(self, train):
        self.trains.add(train)