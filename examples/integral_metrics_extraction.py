from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()
# extract integral metrics ans store it in dictionary
tcx_exercise = tcx_file.read_one_file('path_to_the_file')
integral_metrics = tcx_file.extract_integral_metrics(tcx_exercise)

print(integral_metrics)
