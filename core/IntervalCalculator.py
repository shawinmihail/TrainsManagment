from gui import PlotPane
from core.Objects import Route, GrowthCoeff
import math
from core.SystemBuilder import SystemBuilder
from random import random

class IntervalCalculator:

    @staticmethod
    def cut_negative_value(x):
        if x >= 0:
            return x
        else:
            return 0

    @staticmethod
    def dynamic_func(add_func, tau):
        return lambda t: add_func(t) - add_func(tau * (math.modf(t/tau)[1]))

    @staticmethod
    def next_add_func(add_func, tau, delta):
        return lambda t: IntervalCalculator.cut_negative_value(add_func(tau * (math.modf((t-delta)/tau)[1])))

    @staticmethod
    def find_add_and_dynamic_func(coeff, index, tau_list, delta_list):
        _add_func = lambda t: coeff*t

        for i in range(index):
            _add_func = IntervalCalculator.next_add_func(_add_func, tau_list[i], delta_list[i])

        _dynamic_func = IntervalCalculator.dynamic_func(_add_func, tau_list[index])
        return _add_func, _dynamic_func

    @staticmethod
    def calculate_routs_real_storage_costs(route, time_interval):
        costs = 0
        for dict1 in route.growth_coeffs_list:
            growth_coeff = dict1[Route.COEFFICIENT_HEADER]
            index = dict1[Route.INDEX_HEADER]
            time_in_way_list = dict1[Route.TIME_IN_WAY_LIST_HEADER]
            periods_list = dict1[Route.PERIOD_LIST_HEADER]

            add_func, dynamic_func = IntervalCalculator.find_add_and_dynamic_func(
                growth_coeff.coeff, index, periods_list, time_in_way_list)

            for t in range(time_interval):
                t = t * 0.1
                x = dynamic_func(t)
                costs += x * 0.1

        return costs

    @staticmethod
    def calculate_total_real_storage_costs(time_interval):
        sum = 0
        for route in SystemBuilder.routes:
            sum += IntervalCalculator.calculate_routs_real_storage_costs(route, time_interval)
        return sum

    @staticmethod
    def calculate_period(route):
        sum = 0
        launch_price = route.cost_of_launch
        for dict1 in route.growth_coeffs_list:
            growth_coeff = dict1[Route.COEFFICIENT_HEADER]
            index = dict1[Route.INDEX_HEADER]
            base_station = growth_coeff.way_phases_list[index][0]
            cost_price = SystemBuilder.scheme.node[base_station][SystemBuilder.ATTRIBUTE_STORAGE_PRICE]
            sum += growth_coeff.coeff * cost_price * 0.5

        if sum == 0:
            period = -1
        else:
            period = math.sqrt(launch_price / sum)

        return period

    @staticmethod
    def calculate_and_set_periods():
        for route in SystemBuilder.routes:
            period = IntervalCalculator.calculate_period(route)
            route.period = period


if __name__ == "__main__":
    pass
        # time = list()
        # value = list()
        # for t in range(9999):
        #     t = t*0.1
        #     time.append(t)
        #     x = dynamic_func(t)
        #     value.append(x)
        # PlotPane.draw_2d_plot(time, value)
        # return