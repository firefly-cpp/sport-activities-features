import numpy as np
import sys
sys.path.append('../')

from sport_activities_features.area_identification import AreaIdentifiaction
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file('path_to_the_file')

# Converting the read data to arrays
positions = np.array([*activity['positions']])
distances = np.array([*activity['distances']])
area_coordinates = np.array([[10, 10], [10, 50], [50, 50], [50, 10]])

# Identifying the distance inside the given area
area = AreaIdentifiaction(positions, distances, area_coordinates)
distance_in_area = area.identify_distance_in_area()