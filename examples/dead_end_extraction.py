"""This example presents how to extract dead ends from an activity."""
from sport_activities_features.dead_end_identification import (
    DeadEndIdentification,
)
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_file')
activity = tcx_file.extract_activity_data(tcx_exercise)

# Identifying the dead ends: the way back must stay within 20 m of the
# way out, and a dead end must be at least 500 m long (one way).
Dead_ends = DeadEndIdentification(activity['positions'],
                                  activity['distances'],
                                  tolerance_position=20,
                                  minimum_distance=500)
Dead_ends.identify_dead_ends()

for start, end in Dead_ends.dead_ends:
    start_km = Dead_ends.distances[start] / 1000
    end_km = Dead_ends.distances[end] / 1000
    length = (Dead_ends.distances[end] - Dead_ends.distances[start]) / 2
    print(f'Dead end from {start_km:.2f} km to {end_km:.2f} km '
          f'({length:.0f} m each way)')

# Drawing the dead ends on a map (downloads OpenStreetMap tiles).
Dead_ends.show_map()
