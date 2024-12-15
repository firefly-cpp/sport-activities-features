from sport_activities_features import TCXFile

# read TCX file
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_file')
data = tcx_file.extract_activity_data(tcx_exercise)
