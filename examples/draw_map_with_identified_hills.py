"""This example presents how to draw the elevation profile
with identified hills."""
import matplotlib.pyplot as plt

from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()

tcx_exercise = tcx_file.read_one_file('path_to_the_data')
data = tcx_file.extract_activity_data(tcx_exercise)

# detect hills in data
Hill = HillIdentification(
    data['altitudes'], data['distances'], ascent_threshold=30,
)
Hill.identify_hills()
all_hills = Hill.return_hills()

# draw detected hills, coloured by grade
Map = PlotData()
fig = Map.plot_hills_on_map(data['altitudes'], data['distances'], all_hills)

fig.savefig('hills.png', facecolor=fig.get_facecolor())
plt.show()
