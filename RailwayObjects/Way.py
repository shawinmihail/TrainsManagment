# -*- coding: utf-8 -*-
class Way:

    time_to_pass = None
    stations_on_ends = None
    directs = None

    def __init__(self, st1, st2, time_to_pass):
        self.stations_on_ends = set()
        self.stations_on_ends.add(st1)
        self.stations_on_ends.add(st2)
        self.time_to_pass = time_to_pass

        self.directs = list()
        st_list = list()
        for st in self.stations_on_ends:
            st_list.append(st)

        self.directs.append(st_list)
        self.directs.append(st_list.reverse())

    def __repr__(self):
        return "Way: time to pass - %s, stations_on_ends - %s" %\
               (str(self.time_to_pass), self.stations_on_ends_names())

    def stations_on_ends_names(self):
        names = set()
        for st in self.stations_on_ends:
            names.add(st.name)
        return names