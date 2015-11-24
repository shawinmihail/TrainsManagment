# -*- coding: utf-8 -*-
class Way:

    time_to_pass = None
    stations = None
    direct_property = None

    PROPERTY_ONE_DIRECT = "one_direct"
    PROPERTY_TWO_DIRECT = "two_direct"

    def __init__(self, st1, st2, time_to_pass, property):
        self.stations = list()
        self.stations.append(st1)
        self.stations.append(st2)
        self.time_to_pass = time_to_pass
        assert property == Way.PROPERTY_ONE_DIRECT or property == Way.PROPERTY_TWO_DIRECT
        self.direct_property = property

        self.directs = list()
        st_list = list()
        for st in self.stations:
            st_list.append(st)

        self.directs.append(st_list)
        self.directs.append(st_list.reverse())

    def __repr__(self):
        return "Way: time to pass - %s, stations_on_ends - %s" %\
               (str(self.time_to_pass), self.stations_on_ends_names())

    def stations_on_ends_names(self):
        names = set()
        for st in self.stations:
            names.add(st.name)
        return names