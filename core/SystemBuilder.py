import networkx as nx
import matplotlib.pyplot as plt
from random import random
from core.Objects import Route, GrowthCoeff


class SystemBuilder:

    scheme = nx.Graph()
    routes_scheme = nx.Graph()

    routes = list()
    growth_coeffs = list()

    @staticmethod
    def _launch_cost_func(route): return (1000 + 75 * len(route)) * (2+random())

    @staticmethod
    def _storage_cost_func(): return 5 + random() * 5

    @staticmethod
    def _growth_coef_func(): return 4 * (random() * random()) + 2 * random() + 0.5

    @staticmethod
    def _time_distance_func(): return 0.2 * random() + 0.03

    @staticmethod
    def build_random_brunches(len, first_number=1, second_number=2):
        drop_len_func = lambda len: int(len/4)
        brunch_prob = 0.5
        brunch_list = list()

        for k in range(len-1):
            SystemBuilder.scheme.add_edge(first_number, second_number,
                                          weight=1, time_distance= SystemBuilder._time_distance_func()
                                          )
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

        nx.set_node_attributes(SystemBuilder.scheme, "growth_list", None)
        for num in SystemBuilder.scheme.nodes():
            SystemBuilder.scheme.node[num]["growth_list"] = list()

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
                new_route = Route(way_list, SystemBuilder._launch_cost_func(way_list))
                SystemBuilder.routes.append(new_route)
            k += 1

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
                        new_growth_coeff = GrowthCoeff(SystemBuilder._growth_coef_func(), way_list)
                        destination_is_founded = True
                        SystemBuilder.growth_coeffs.append(new_growth_coeff)
                        SystemBuilder.scheme.node[dispatch_st_num]['growth_list'].append(new_growth_coeff)
                    except nx.exception.NetworkXError:
                        pass
                    except nx.exception.NetworkXNoPath:
                        pass

    @staticmethod
    def create_routes_scheme():
        for route in SystemBuilder.routes:
            SystemBuilder.routes_scheme.add_path(route.route_list)

    @staticmethod
    def find_routes_of_load_growthes():

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
            sum_rating = 0
            route_num_list = list()
            while sum_rating != len(coeff.way_list):
                rating, route_num = find_better_route(coeff.way_list[sum_rating:])
                sum_rating += rating
                route_num_list.append(route_num)
            coeff.route_index_list = route_num_list
            print(route_num_list)
            for route_num in route_num_list:
                print(route_num_list.index(route_num))
                SystemBuilder.routes[route_num].load_growth_list.append(
                    {"coeff": coeff, "yard": route_num_list.index(route_num)})

    @staticmethod
    def get_random_element(list1):
        index = int(random() * len(list1)) + 1
        return list1[index]

    @staticmethod
    def set_random_launch_costs():
        for route in SystemBuilder.routes:
            route.cost_of_launch = SystemBuilder._launch_cost_func(route)

    @staticmethod
    def set_random_storage_costs():
        nx.set_node_attributes(SystemBuilder.scheme, "storage_cost", None)
        for num in SystemBuilder.scheme.nodes():
            SystemBuilder.scheme.node[num]["storage_cost"] = SystemBuilder._storage_cost_func()

    @staticmethod
    def create_random_system():
        SystemBuilder.build_random_brunches(14)
        SystemBuilder.build_random_routes(10, 6)
        SystemBuilder.create_routes_scheme()
        SystemBuilder.set_random_loads(10)
        SystemBuilder.find_routes_of_load_growthes()

    @staticmethod
    def plot_sheme():
        nx.draw_networkx(SystemBuilder.scheme, with_labels=True)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    SystemBuilder.create_random_system()