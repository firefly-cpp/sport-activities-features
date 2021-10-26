from sport_activities_features import ElevationIdentification
from sport_activities_features import TCXFile

tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file('path_to_file')

elevations = ElevationIdentification(tcx_data['positions'])
tcx_data.update({'elevations':elevations})