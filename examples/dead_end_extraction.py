"""This example presents how to extract dead ends from an activity."""
import numpy as np

from sport_activities_features.dead_end_identification import (
    DeadEndIdentification,
)
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_file')
activity = tcx_file.extract_activity_data(tcx_exercise)

# Converting the read data to the array.
positions = np.array([*activity['positions']])
distances = np.array([*activity['distances']])

# Identifying the dead ends.
Dead_ends = DeadEndIdentification(positions,
                                  distances,
                                  tolerance_degrees=1,
                                  tolerance_position=2,
                                  minimum_distance=500)
Dead_ends.identify_dead_ends()
Dead_ends.show_map()
