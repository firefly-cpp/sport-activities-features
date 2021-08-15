import sys

sys.path.append("../")

from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()
# extract integral metrics ans store it in dictionary
integral_metrics = tcx_file.extract_integral_metrics("path_to_the_file")

print(integral_metrics)
