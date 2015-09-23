from gui import PlotPane
import math
from random import random

alpha = 2
tau_list = [15, 10, 40, 9, 8, 7, 5]
# tau_list = [10*random() for x in range(10)]

def dynamic_func(add_func, tau):
    return lambda t: add_func(t) - add_func(tau * (math.modf(t/tau)[1]))

def next_add_func(add_func, tau):
    return lambda t: add_func(tau * (math.modf(t/tau)[1]))

def station_n_dynamic_funct(n, tau_list):
    _add_func = lambda t: alpha*t

    for i in range(n):
        _add_func = next_add_func(_add_func, tau_list[i])

    _dynamic_func = dynamic_func(_add_func, tau_list[n])

    return _add_func, _dynamic_func


if __name__ == "__main__":
    k = 6
    a, d = station_n_dynamic_funct(k, tau_list)
    time = list()
    value = list()
    n = 5000
    sum = 0
    for t in range(n):
        t = t*0.1
        time.append(t)
        x = d(t)
        sum += x
        value.append(x)
    print(sum/(tau_list[k]*n))
    PlotPane.draw(time, value)

