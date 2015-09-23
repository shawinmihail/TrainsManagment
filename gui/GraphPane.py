import networkx as nx
import matplotlib.pyplot as plt
from random import random


def build_brunch(graph, len, first_number=1, second_number=2):
    drop_len_func = lambda len: int(len/4)
    brunch_prob = 0.5
    brunch_list = list()

    for k in range(len-1):
        graph.add_edge(first_number, second_number, weight=1)
        if random() < brunch_prob:
            brunch_list.append(first_number)
        first_number = second_number
        second_number += 1

    try:
        if build_brunch.max < second_number:
            build_brunch.max = second_number
    except AttributeError:
        build_brunch.max = second_number

    for number in brunch_list:
        build_brunch(graph, drop_len_func(len), first_number=number, second_number=build_brunch.max)

scheme = nx.Graph()
build_brunch(scheme, 12)
print(scheme.nodes())
print(scheme.edges())
nx.draw_networkx(scheme, with_labels=True)
limits = plt.axis('off')
plt.show()