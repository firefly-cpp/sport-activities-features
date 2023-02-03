"""
This example presents how to convert a TCX file to a GPX file.
The file is saved in the same directory as the original file.
"""
from sport_activities_features.tcx_manipulation import TCXFile

tcx_file = TCXFile()

tcx_file.convert_tcx_to_gpx("path_to_original_file", output_file_name=None)
