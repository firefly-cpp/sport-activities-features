"""This example presents how to draw a map with identified hills."""
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()

data = tcx_file.read_one_file('C:/Users/Zala/Documents/sport-activities-features/sport-activities-features/tests/data/15.tcx')

# detect hills in data
Hill = HillIdentification(data['altitudes'], 30)
Hill.identify_hills()
all_hills = Hill.return_hills()

# draw detected hills
Map = PlotData()

Map.draw_hills_in_map(data['altitudes'], data['distances'], all_hills)
