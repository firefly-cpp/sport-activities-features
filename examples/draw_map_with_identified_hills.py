"""This example presents how to draw a map with identified hills."""
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()

data = tcx_file.read_one_file('path_to_the_data')

# detect hills in data
Hill = HillIdentification(data['altitudes'], 30)
Hill.identify_hills()
all_hills = Hill.return_hills()

# draw detected hills
Map = PlotData()

Map.show_hills_on_map(data['altitudes'], data['distances'], all_hills)
