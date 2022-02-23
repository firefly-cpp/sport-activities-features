import os

from sport_activities_features.data_extraction import DataExtraction
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
)
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures


# Retrieving all TCX files in a directory
tcx_file = TCXFile()
all_files = tcx_file.read_directory('path_to_the_folder')

# Extracting the data of all files
activities = []
for file in all_files:
    activity = {'ID': os.path.splitext(os.path.split(file)[-1])[0]}
    activity.update(tcx_file.read_one_file(file))
    activity.update(tcx_file.extract_integral_metrics(file))

    # Hills
    Hill = HillIdentification(activity['altitudes'], 30)
    Hill.identify_hills()
    all_hills = Hill.return_hills()
    Top = TopographicFeatures(all_hills)
    num_hills = Top.num_of_hills()
    distance_hills = Top.distance_of_hills(activity['positions'])
    distance_between_hills = activity['distance'] - distance_hills

    activity.update(
        {'number_of_hills': num_hills,
         'distance_between_hills': distance_between_hills}
    )

    # Identifying the intervals in the activity by heart rate
    # Since a lot of TCX files contain invalid data,
    # intervals cannot be identified, thus those activities
    # cannot be extracted to CSV
    try:
        Intervals = IntervalIdentificationByHeartRate(
            activity['distances'],
            activity['timestamps'],
            activity['altitudes'],
            activity['heartrates'],
        )
        Intervals.identify_intervals()
        all_intervals = Intervals.return_intervals()
        activity.update(Intervals.calculate_interval_statistics())
    except Exception:
        continue

    activities.append(activity)

# Extracting the data in CSV format
data_extraction = DataExtraction(activities)
data_extraction.extract_data('name_of_the_csv_file')
