from sport_activities_features import TCXFile

# read TCX file
tcx_file = TCXFile()
data = tcx_file.read_one_file('path_to_the_file')
