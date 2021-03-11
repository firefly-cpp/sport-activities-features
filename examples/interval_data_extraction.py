import sys
sys.path.append('../')

from sport_activities_features.interval_identification import IntervalIdentificationByPower, IntervalIdentificationByHeartrate
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file("path_to_the_data")

# Identifying the intervals in the activity by power
Intervals = IntervalIdentificationByPower(activity["distances"], activity["timestamps"], activity["altitudes"], 70)
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()

# Identifying the intervals in the activity by heart rate
Intervals = IntervalIdentificationByHeartrate(activity["distances"], activity["timestamps"], activity["altitudes"], activity["heartrates"])
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()