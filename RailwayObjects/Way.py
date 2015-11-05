# -*- coding: utf-8 -*-
class Way:

    time_len = None
    stations_on_ends = None

    def __init__(self, pair_of_stations, time_len):
        self.stations_on_ends = pair_of_stations
        self.time_len = time_len


