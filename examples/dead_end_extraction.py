"""
This example presents how to extract dead ends from an exercise.
"""

import numpy as np
import sys

sys.path.append("../")

from sport_activities_features.dead_end_identification import DeadEndIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
tcx_file = TCXFile()
activity = tcx_file.read_one_file('../datasets/15.tcx')

# Converting the read data to the array.
positions = np.array([*activity['positions']])
distances = np.array([*activity['distances']])

# Identifying the dead ends.
Dead_ends = DeadEndIdentification(positions, distances)
Dead_ends.identify_dead_ends()
Dead_ends.draw_map()