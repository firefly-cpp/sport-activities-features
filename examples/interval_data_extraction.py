"""This example presents how to use interval identification
based by power and by heart rate.
"""
from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
    IntervalIdentificationByPower,
)
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_data')
activity = tcx_file.extract_activity_data(tcx_exercise)

# Identifying the intervals in the activity by power
Intervals = IntervalIdentificationByPower(
    activity['distances'],
    activity['timestamps'],
    activity['altitudes'],
    mass=70,
)
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()

# Identifying the intervals in the activity by heart rate
Intervals = IntervalIdentificationByHeartRate(
    activity['distances'],
    activity['timestamps'],
    activity['altitudes'],
    activity['heartrates'],
)
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()
