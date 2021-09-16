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
all_files = tcx_file.read_directory("../datasets")

areas = np.array([])
progress = 0.0

# Reading all files in filder.
for file in all_files:
    print('\rProgress: ', int(progress), '%', end='')
    activity = tcx_file.read_one_file(file)

    # Converting the read data to arrays.
    positions = np.array([*activity['positions']])
    distances = np.array([*activity['distances']])
    timestamps = np.array([*activity['timestamps']])
    heartrates = np.array([*activity['heartrates']])

    # Area coordinates should be given in clockwise orientation in the form of 3D array (number_of_hulls, hull_coordinates, 2).
    # Holes in area are permitted.
    area_coordinates = np.array([[[45.530643, 13.706290], [45.570553, 13.744146], [45.554449, 13.789791], [45.534131, 13.751618], [45.543990, 13.735831], [45.524630, 13.742444]]])

    # Extracting the data inside the given area.
    area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
    area.identify_points_in_area()
    area_data = area.extract_data_in_area()
    if area_data['distance'] != 0.0:
        areas = np.append(areas, area)

    area.draw_map()
    progress += 100 / len(all_files)

print('\rProgress: 100 %')
AreaIdentification.draw_activities_inside_area_on_map(areas, area_coordinates)