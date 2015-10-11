import matplotlib
matplotlib.use("Qt5Agg")
from core.SystemBuilder import SystemBuilder as SB
from core.IntervalCalculator import IntervalCalculator as IC

SB.create_random_system()
print(IC.calculate_total_real_storage_costs(999))
IC.calculate_and_set_periods()
SB.set_period_and_time_in_way_lists()
print(IC.calculate_total_real_storage_costs(999))
SB.change_periods_in(2)
SB.set_period_and_time_in_way_lists()
print(IC.calculate_total_real_storage_costs(999))
SB.change_periods_in(0.25)
SB.set_period_and_time_in_way_lists()
print(IC.calculate_total_real_storage_costs(999))
