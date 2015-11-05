class Route:

    route_list = list()
    cost_of_launch = 0
    period = 0

    COEFFICIENT_HEADER = "coeff"
    INDEX_HEADER = "index"
    TIME_IN_WAY_LIST_HEADER = "time_in_way_list"
    PERIOD_LIST_HEADER = "period_list"
    growth_coeffs_list = None

    def __init__(self, route, cost_of_launch=0, period=0):
        self.route_list = route
        self.cost_of_launch = cost_of_launch
        self.period = period
        self.growth_coeffs_list = list()

    def __str__(self):
        return str(self.route_list)

    def __repr__(self):
        return str(self.route_list)

    def length(self):
        return len(self.route_list)

    def add_to_growth_coeffs_list(self, coeff, index):
        dict1 = dict()
        dict1[self.COEFFICIENT_HEADER] = coeff
        dict1[self.INDEX_HEADER] = index
        dict1[self.PERIOD_LIST_HEADER] = None
        dict1[self.TIME_IN_WAY_LIST_HEADER] = None
        self.growth_coeffs_list.append(dict1)


class GrowthCoeff:

    coeff = 0
    way_list = None
    # numbers of routes in routes list of SystemBuilder in true order
    route_index_list = None
    # list of sequences of stations, each sequence contain stations from one route, in true order
    way_phases_list = None

    def __init__(self, coeff, way_list):
        self.coeff = coeff
        self.way_list = way_list
        self.route_index_list = list()
        self.way_phases_list = list()

    def __str__(self):
        return "GrowthCoeff(%s, disp: %s, dest: %s)" % (str(self.coeff), str(self.way_list[0]), str(self.way_list[-1]))

    def __repr__(self):
        return "GrowthCoeff(%s, disp: %s, dest: %s)" % (str(self.coeff), str(self.way_list[0]), str(self.way_list[-1]))