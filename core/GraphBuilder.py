import networkx as nx
import matplotlib.pyplot as plt
from random import random


class GraphBuilder:

    scheme = nx.Graph()
    routes = list()

    @staticmethod
    def build_random_brunches(len, first_number=1, second_number=2):
        drop_len_func = lambda len: int(len/4)
        brunch_prob = 0.5
        brunch_list = list()

        for k in range(len-1):
            GraphBuilder.scheme.add_edge(first_number, second_number, weight=1)
            if random() < brunch_prob:
                brunch_list.append(first_number)
            first_number = second_number
            second_number += 1

        try:
            if GraphBuilder.build_random_brunches.max < second_number:
                GraphBuilder.build_random_brunches.max = second_number
        except AttributeError:
            GraphBuilder.build_random_brunches.max = second_number

        for number in brunch_list:
            GraphBuilder.build_random_brunches(
                drop_len_func(len), first_number=number, second_number=GraphBuilder.build_random_brunches.max)

    @staticmethod
    def build_random_routes(max_len, number):
        scheme_len = len(GraphBuilder.scheme.nodes())
        for k in range(number):
            station_number = int(random() * scheme_len)
            print(nx.shortest_path(GraphBuilder, station_number, 1))

if __name__ == '__main__':
    GraphBuilder.build_random_brunches(12)
    GraphBuilder.build_random_routes(1, 1)
    nx.draw_networkx(GraphBuilder.scheme, with_labels=True)
    limits = plt.axis('off')
    plt.show()