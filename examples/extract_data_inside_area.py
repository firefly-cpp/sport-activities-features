"""
This example presents how to extract data inside the area given with coordinates.
"""

import numpy as np
import sys

sys.path.append("../")

from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
tcx_file = TCXFile()
activity = tcx_file.read_one_file("path_to_the_data")

# Converting the read data to arrays.
positions = np.array([*activity["positions"]])
distances = np.array([*activity["distances"]])
timestamps = np.array([*activity["timestamps"]])
heartrates = np.array([*activity["heartrates"]])

# Area coordinates should be given in clockwise orientation in the form of 3D array (number_of_hulls, hull_coordinates, 2).
# Holes in area are permitted.
area_coordinates = np.array(
    [[[10, 10], [10, 50], [50, 50], [50, 10]], [[19, 19], [19, 21], [21, 21], [21, 19]]]
)

# Extracting the data inside the given area.
area = AreaIdentification(
    positions, distances, timestamps, heartrates, area_coordinates
)
area.identify_points_in_area()
area_data = area.extract_data_in_area()
