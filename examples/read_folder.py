from sport_activities_features.tcx_manipulation import TCXFile

# get all TCX files in a directory
tcx_file = TCXFile()
all_files = tcx_file.read_directory('path_to_the_folder')

# iterate through files and print total distance of activities
for i in range(len(all_files)):
    tcx_exercise = tcx_file.read_one_file(all_files[i])
    activity = tcx_file.extract_activity_data(tcx_exercise)
    print('total distance: ', activity['total_distance'] / 1000)
