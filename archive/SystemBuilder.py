from random import random

import networkx as nx
import matplotlib.pyplot as plt

from core import RandomFunctions
from archive.Objects import Route, GrowthCoeff


class SystemBuilder:

    ATTRIBUTE_GROWTH_LIST = "growth_list"
    ATTRIBUTE_STORAGE_PRICE = "storage_cost"
    ATTRIBUTE_TIME_IN_WAY = "time_in_way"

    scheme = nx.Graph()
    routes_scheme = nx.Graph()

    routes = list()
    growth_coeffs = list()

    @staticmethod
    def build_random_brunches(len, first_number=1, second_number=2):
        drop_len_func = lambda len: int(len/4)
        brunch_prob = 0.5
        brunch_list = list()

        for k in range(len-1):
            SystemBuilder.scheme.add_edge(first_number, second_number, weight=1)
            SystemBuilder.scheme[first_number][second_number][SystemBuilder.ATTRIBUTE_TIME_IN_WAY] = RandomFunctions.time_distance_func()
            if random() < brunch_prob:
                brunch_list.append(first_number)
            first_number = second_number
            second_number += 1

        try:
            if SystemBuilder.build_random_brunches.max < second_number:
                SystemBuilder.build_random_brunches.max = second_number
        except AttributeError:
            SystemBuilder.build_random_brunches.max = second_number

        for number in brunch_list:
            SystemBuilder.build_random_brunches(
                drop_len_func(len), first_number=number, second_number=SystemBuilder.build_random_brunches.max)

        attr_name = SystemBuilder.ATTRIBUTE_GROWTH_LIST
        nx.set_node_attributes(SystemBuilder.scheme, attr_name, None)
        for num in SystemBuilder.scheme.nodes():
            SystemBuilder.scheme.node[num][attr_name] = list()

    @staticmethod
    def build_random_routes(attempts_num, min_len):
        scheme_len = len(SystemBuilder.scheme.node)
        k = 0
        while k < attempts_num:
            first_station_number = int(random() * scheme_len) + 1
            second_station_number = int(random() * scheme_len) + 1
            way_len, way_list = \
                nx.bidirectional_dijkstra(SystemBuilder.scheme, first_station_number, second_station_number)
            if way_len >= min_len:
                way_list = way_list + way_list[::-1][1:]
                new_route = Route(way_list, RandomFunctions.launch_cost_func(way_list))
                SystemBuilder.routes.append(new_route)
            k += 1

        SystemBuilder._create_routes_scheme()

    @staticmethod
    def _create_routes_scheme():
        for route in SystemBuilder.routes:
            SystemBuilder.routes_scheme.add_path(route.route_list)

    @staticmethod
    def set_random_loads(max_for_each_route):
        scheme_len = len(SystemBuilder.scheme.node)
        for route in SystemBuilder.routes:
            for k in range(int(random() * max_for_each_route)):

                dispatch_st_num = route.route_list[int(random() * route.length())]

                destination_is_founded = False
                counter = 0
                while not destination_is_founded:
                    counter += 1
                    assert counter < 999
                    destination_st_num = int(random() * scheme_len) + 1
                    try:
                        way_length, way_list = nx.bidirectional_dijkstra(
                            SystemBuilder.routes_scheme, dispatch_st_num, destination_st_num)
                        new_growth_coeff = GrowthCoeff(RandomFunctions.growth_coef_func(), way_list)
                        destination_is_founded = True
                        SystemBuilder.growth_coeffs.append(new_growth_coeff)
                        attr_name = SystemBuilder.ATTRIBUTE_GROWTH_LIST
                        SystemBuilder.scheme.node[dispatch_st_num][attr_name].append(new_growth_coeff)
                    except nx.exception.NetworkXError:
                        pass
                    except nx.exception.NetworkXNoPath:
                        pass

    @staticmethod
    def _find_routes_for_load_factories():

        def is_slice_in_list(l, l0):
            len_s = len(l)
            return any(l == l0[i:len_s+i] for i in range(len(l0) - len_s+1))
        
        def find_better_route(way_part):
            rating_list = list()
            for r_num in range(len(SystemBuilder.routes)):
                route = SystemBuilder.routes[r_num]
                rating = 0
                for k in range(len(way_part)):
                    if is_slice_in_list(way_part[:k+1], route.route_list):
                        rating += 1
                    else:
                        break

                rating_list.append(rating)
            return max(rating_list), rating_list.index(max(rating_list))

        for coeff in SystemBuilder.growth_coeffs:
            disp = coeff.way_list[0]
            dest = coeff.way_list[-1]
            head = disp
            sum_rating = 0
            route_num_list = list()
            way_phases_list = list()
            iterations_counter = 0
            while head != dest:
                iterations_counter += 1
                assert iterations_counter < 999
                way_part = coeff.way_list[sum_rating:]
                rating, route_num = find_better_route(way_part)
                way_phases_list.append(way_part[:rating])
                head = way_part[rating-1]
                route_num_list.append(route_num)
                sum_rating += rating -1
            coeff.route_index_list = route_num_list
            coeff.way_phases_list = way_phases_list
            for route_num in route_num_list:
                SystemBuilder.routes[route_num].add_to_growth_coeffs_list(coeff, route_num_list.index(route_num))

    @staticmethod
    def set_random_launch_costs():
        for route in SystemBuilder.routes:
            route.cost_of_launch = RandomFunctions.launch_cost_func(route.route_list)

    @staticmethod
    def set_random_storage_costs():
        attr_name = SystemBuilder.ATTRIBUTE_STORAGE_PRICE
        nx.set_node_attributes(SystemBuilder.scheme, attr_name, None)
        for num in SystemBuilder.scheme.nodes():
            SystemBuilder.scheme.node[num][attr_name] = RandomFunctions.storage_cost_func()

    @staticmethod
    def set_random_launch_periods():
        for route in SystemBuilder.routes:
            route.period = RandomFunctions.period_func()

    @staticmethod
    def set_period_and_time_in_way_lists():
        for route in SystemBuilder.routes:
            for k in range(len(route.growth_coeffs_list)):
                period_list = list()
                time_in_way_list = list()
                coeff = route.growth_coeffs_list[k][Route.COEFFICIENT_HEADER]

                for i in range(len(coeff.route_index_list)):
                    period_list.append(SystemBuilder.routes[i].period)
                route.growth_coeffs_list[k][Route.PERIOD_LIST_HEADER] = period_list

                for line in coeff.way_phases_list:
                    time_in_way = 0
                    for st_num in range(len(line)-1):
                        time_in_way += SystemBuilder.scheme[st_num+1][st_num+2][SystemBuilder.ATTRIBUTE_TIME_IN_WAY]
                    time_in_way_list.append(time_in_way)

                route.growth_coeffs_list[k][Route.TIME_IN_WAY_LIST_HEADER] = time_in_way_list

    @staticmethod
    def change_periods_in(times):
        for route in SystemBuilder.routes:
            route.period *= times

    @staticmethod
    def remove_useless_routes():
        pass

    @staticmethod
    def create_random_system():
        SystemBuilder.build_random_brunches(14)
        SystemBuilder.build_random_routes(10, 6)
        SystemBuilder.create_routes_scheme()
        SystemBuilder.set_random_launch_periods()
        SystemBuilder.set_random_loads(10)
        SystemBuilder.find_routes_for_load_factories()
        SystemBuilder.set_random_storage_costs()
        SystemBuilder.set_random_launch_costs()
        SystemBuilder.set_period_and_time_in_way_lists()

        # for coeff in SystemBuilder.growth_coeffs:
        #     print(coeff)
        #     print(coeff.way_phases_list)
        #     print("---------------")

    @staticmethod
    def plot_scheme():
        nx.draw_networkx(SystemBuilder.scheme, with_labels=True)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    SystemBuilder.create_random_system()