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
all_files = tcx_file.read_directory('path_to_the_directory')

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

    # Area coordinates should be given in clockwise orientation in the form of a 3D array (number_of_hulls, hull_coordinates, 2).
    # Holes in the area are permitted.
    area_coordinates = np.array([[[47.530643, 15.706290], [47.570553, 15.744146], [47.554449, 15.789791], [47.534131, 15.751618], [47.543990, 15.735831], [47.524630, 15.742444]]])

    # Extracting the data inside the given area.
    area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
    area.identify_points_in_area()
    area_data = area.extract_data_in_area()
    if area_data['distance'] != 0.0:
        areas = np.append(areas, area)

    # Drawing a map of the activity and updating the progress.
    area.draw_map()
    progress += 100 / len(all_files)

# Drawing a map of all the activities or their parts inside of the chosen area.
print('\rProgress: 100 %')
AreaIdentification.draw_activities_inside_area_on_map(areas, area_coordinates)