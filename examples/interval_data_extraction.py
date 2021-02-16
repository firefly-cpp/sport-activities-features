import sys
sys.path.append('../')

from sport_activities_features.interval_identification import IntervalIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# Reading TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file("../datasets/15.tcx")

# Searching for intervals in the activity
Intervals = IntervalIdentification(activity["distances"], activity["timestamps"], activity["altitudes"], 30)
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()