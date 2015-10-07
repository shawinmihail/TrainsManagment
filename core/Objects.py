

class Route:

    route_list = list()
    cost_of_launch = 0
    period = 0

    def __init__(self, route, cost_of_launch=0, period=0):
        self.route_list = route
        self.cost_of_launch = cost_of_launch
        self.period = period

    def __str__(self):
        return str(self.route_list)

    def __repr__(self):
        return str(self.route_list)

    def length(self):
        return len(self.route_list)


class GrowthCoeff:

    coeff = 0
    way_list = list()
    loads_list = list()

    def __init__(self, coeff, way_list):
        self.coeff = coeff
        self.way_list = way_list

    def __str__(self):
        return "[coeff: %s, destination: %s]" % (str(self.coeff), str(self.way_list[-1]))

    def __repr__(self):
        return "[coeff: %s, destination: %s]" % (str(self.coeff), str(self.way_list[-1]))