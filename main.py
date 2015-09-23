from gui import PlotPane
import math
from random import random

alpha = 1
tau_list = [2, 3, 4, 5, 4, 3, 2]
# tau_list = [10*random() for x in range(10)]
delta_list = [3, 3, 1, 1, 1, 1]

def positivator(x):
    if x >= 0:
        return x
    else:
        return 0


def dynamic_func(add_func, tau):
    return lambda t: add_func(t) - add_func(tau * (math.modf(t/tau)[1]))

def next_add_func(add_func, tau, delta):
    return lambda t: positivator(add_func(tau * (math.modf((t-delta)/tau)[1])))

def station_n_dynamic_funct(n, tau_list, delta_list):
    _add_func = lambda t: alpha*t

    for i in range(n):
        _add_func = next_add_func(_add_func, tau_list[i], delta_list[i])

    _dynamic_func = dynamic_func(_add_func, tau_list[n])

    return _add_func, _dynamic_func


if __name__ == "__main__":
    print(math.modf(15/2)[1])
    # k = 1
    # a, d = station_n_dynamic_funct(k, tau_list, delta_list)
    # time = list()
    # value = list()
    # n = 100
    # sum = 0
    # for t in range(n):
    #     t = t*0.1
    #     time.append(t)
    #     x = d(t)
    #     sum += x
    #     value.append(x)
    # print(sum/(tau_list[k]*n))
    # PlotPane.draw_2d_plot(time, value)

