"""
This example presents how to extract data inside the area given with coordinates.
"""

import numpy as np
import sys
from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
sys.path.append("../")
tcx_file = TCXFile()
#all_files = tcx_file.read_directory('path_to_the_directory')
all_files = tcx_file.read_directory('../datasets')

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
    area_coordinates = np.array([[[45.445539, 13.736101], [45.566894, 13.700517], [45.563605, 13.806872], [45.480111, 13.812463]]])

    # Extracting the data inside of the given area.
    area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
    area.identify_points_in_area()
    area_data = area.extract_data_in_area()

    # If at least a part of exercise is inside of the area, the area is added to the array of areas.
    if area_data['distance'] != 0.0:
        areas = np.append(areas, area)

    # Drawing a map of the activity and updating the progress.
    area.draw_map()
    progress += 100 / len(all_files)

# Drawing a map of all the activities or their parts inside of the chosen area.
print('\rProgress: 100 %')
AreaIdentification.draw_activities_inside_area_on_map(areas, area_coordinates)