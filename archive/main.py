import matplotlib
matplotlib.use("Qt5Agg")
from archive.SystemBuilder import SystemBuilder as SB
from archive.IntervalCalculator import IntervalCalculator as IC
from Gui import PlotPane
import math

k_list = list()
v_list = list()

SB.create_random_system()
IC.calculate_and_set_periods()
SB.change_periods_in(0.125)
SB.set_period_and_time_in_way_lists()
k = math.pow(2, -6)
for i in range(9):
    k_list.append(k)
    v = IC.calculate_total_real_storage_costs(999)
    v_list.append(v)
    k *= 2
    SB.change_periods_in(2)
    SB.set_period_and_time_in_way_lists()

PlotPane.draw_2d_plot(k_list, v_list)