from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures

# read TCX file
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_data')
activity = tcx_file.extract_activity_data(tcx_exercise)

# detect hills in data
Hill = HillIdentification(activity['altitudes'], 30)
Hill.identify_hills()
all_hills = Hill.return_hills()

# extract features from data
Top = TopographicFeatures(all_hills)
num_hills = Top.num_of_hills()
avg_altitude = Top.avg_altitude_of_hills(activity['altitudes'])
avg_ascent = Top.avg_ascent_of_hills(activity['altitudes'])
distance_hills = Top.distance_of_hills(activity['positions'])
hills_share = Top.share_of_hills(distance_hills, activity['total_distance'])

print('num hills: ', num_hills)
print('avg_altitude: ', avg_altitude)
print('avg_ascent: ', avg_ascent)
print('total distance: ', activity['total_distance'] / 1000)
print('distance_hills: ', distance_hills)
print('hills_share: ', hills_share)
