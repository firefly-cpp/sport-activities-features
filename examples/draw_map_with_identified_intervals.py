"""This example presents how to plot identified intervals."""
import matplotlib.pyplot as plt

from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
    IntervalIdentificationByPower,
)
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_data')
activity = tcx_file.extract_activity_data(tcx_exercise)
altitudes = activity['altitudes']
distances = activity['distances']
timestamps = activity['timestamps']
heartrates = activity['heartrates']

Map = PlotData()

# Identifying the intervals in the activity by heart rate and plotting them
# over the heart rate
Intervals = IntervalIdentificationByHeartRate(
    distances, timestamps, altitudes, heartrates,
)
Intervals.identify_intervals()
fig = Map.plot_intervals_in_map(
    timestamps, Intervals.return_intervals(), values=heartrates,
)
fig.savefig('intervals_heart_rate.png', facecolor=fig.get_facecolor())

# Identifying the intervals in the activity by power and plotting them over
# the estimated power (smoothed over 30 s)
Intervals = IntervalIdentificationByPower(distances, timestamps, altitudes, 70)
Intervals.identify_intervals()
fig = Map.plot_intervals_in_map(
    timestamps, Intervals.return_intervals(), values=Intervals.powers,
    value_label='Power', value_unit='W', smoothing=30,
)
fig.savefig('intervals_power.png', facecolor=fig.get_facecolor())

plt.show()
