# sport-activities-features --- A minimalistic toolbox for extracting features from sport activity files written in Python

---

[![PyPI Version](https://img.shields.io/pypi/v/sport-activities-features.svg)](https://pypi.python.org/pypi/sport-activities-features)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sport-activities-features.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sport-activities-features.svg)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/sport-activities-features.svg)](https://github.com/firefly-cpp/sport-activities-features/blob/master/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/sport-activities-features.svg)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/sport-activities-features.svg)](http://isitmaintained.com/project/firefly-cpp/sport-activities-features "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/sport-activities-features.svg)](http://isitmaintained.com/project/firefly-cpp/sport-activities-features "Percentage of issues still open")
![GitHub contributors](https://img.shields.io/github/contributors/firefly-cpp/sport-activities-features.svg)

## Objective
Data analysis of sport activities that were monitored by the use of [sport trackers is popular](http://iztok-jr-fister.eu/static/publications/42.pdf).
Many interesting utilizations of data are available, e.g. large-scale data mining of sport activities files for the [automatic sport training sessions generation](http://iztok-jr-fister.eu/static/publications/189.pdf).

Most of the available solutions nowadays are relied upon integral metrics such as total duration, total distance, average hearth rate, etc. However,
such solutions may suffer of "overall (integral) metrics problem", commonly associated with following biases:
- details not expressed sufficiently,
- general/integral outlook of the race/training captured only,
- possibly fallacious intensity metrics of performed race/training and
- not recognized different stages/phases of the sport race/training, i.e. warming-up, endurance, intervals, etc.

Proposed software supports the extraction of following topographic features from sport activity files:
- number of hills,
- average altitude of identified hills,
- total distance of identified hills,
- climbing ratio (total distance of identified hills vs. total distance),
- average ascent of hills
- total ascent
- total descent
- and many others.


## Installation

### pip3

Install sport-activities-features with pip3:

```sh
pip3 install sport-activities-features
```

### Fedora Linux

To install sport-activities-features on Fedora, use:

```sh
$ dnf install python3-sport-activities-features
```

## Full Features

- Extraction of integral metrics (total distance, total duration, calories) ([see example](examples/integral_metrics_extraction.py))
- Extraction of topographic features (number of hills, average altitude of identified hills, total distance of identified hills, climbing ratio, average ascent of hills, total ascent, total descent) ([see example](examples/hill_data_extraction.py))
- Plotting the identified hills ([see example](examples/draw_map_with_identified_hills.py)) 
- Extraction of intervals (number of intervals, maximum/minimum/average duration of intervals, maximum/minimum/average distance of intervals, maximum/minimum/average heart rate during intervals)
- Plotting the identified intervals ([see example](examples/draw_map_with_identified_intervals.py)) 
- Calculation of training loads (Bannister TRIMP, Lucia TRIMP) ([see example](examples/integral_metrics_extraction.py))
- Compatible with TCX activity files and [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) nodes
- Parsing of Historical weather data from an external service
- Extraction of integral metrics of the activity inside area given with coordinates (distance, heartrate, speed) ([see example](examples/extract_data_inside_area.py))
- Extraction of activities from CSV file(s) and random selection of a specific number of activities ([see example](examples/extract_random_activities_from_csv.py))

## Historical weather data
Weather data parsed is collected from the [Visual Crossing Weather API](https://www.visualcrossing.com/). 
This is an external unaffiliated service and the user must register and use the API key provided from the service. 
The service has a free tier (1000 Weather reports / day) but is otherwise operating on a pay as you go model.
For the pricing and terms of use please read the [official documentation](https://www.visualcrossing.com/weather-data-editions) of the API provider.

## Overpass API & Open Elevation API integration
Without performed activities we can use the [OpenStreetMap](https://www.openstreetmap.org/) for identification of hills,
total ascent and descent. This is done using the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
which is a read-only API that allows querying of OSM map data. In addition to that altitude data is retrieved by using the
[Open-Elevation API](https://open-elevation.com/) which is a open-source and free alternative to the Google Elevation API.
Both of the solutions can be used by using free publicly acessible APIs ([Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API), [Open-Elevation](https://open-elevation.com/#public-api)) or can be self hosted on a server or as a Docker container ([Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API/Installation), [Open-Elevation](https://github.com/Jorl17/open-elevation/blob/master/docs/host-your-own.md)).

## CODE EXAMPLES:

### Extraction of topographic features
```python
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.plot_data import PlotData

# Read TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file("path_to_the_file")

# Detect hills in data
Hill = HillIdentification(activity['altitudes'], 30)
Hill.identify_hills()
all_hills = Hill.return_hills()

# Extract features from data
Top = TopographicFeatures(all_hills)
num_hills = Top.num_of_hills()
avg_altitude = Top.avg_altitude_of_hills(activity['altitudes'])
avg_ascent = Top.avg_ascent_of_hills(activity['altitudes'])
distance_hills = Top.distance_of_hills(activity['positions'])
hills_share = Top.share_of_hills(distance_hills, activity['total_distance'])
```

### Extraction of intervals
```python
import sys
sys.path.append('../')

from sport_activities_features.interval_identification import IntervalIdentificationByPower, IntervalIdentificationByHeartrate
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file("path_to_the_data")

# Identifying the intervals in the activity by power
Intervals = IntervalIdentificationByPower(activity["distances"], activity["timestamps"], activity["altitudes"], 70)
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()

# Identifying the intervals in the activity by heart rate
Intervals = IntervalIdentificationByHeartrate(activity["timestamps"], activity["altitudes"], activity["heartrates"])
Intervals.identify_intervals()
all_intervals = Intervals.return_intervals()
```

### Extraction of integral metrics
```python
import sys
sys.path.append('../')

from sport_activities_features.tcx_manipulation import TCXFile

# Read TCX file
tcx_file = TCXFile()

integral_metrics = tcx_file.extract_integral_metrics("path_to_the_file")

print(integral_metrics)

```

### Weather data extraction
```python
from sport_activities_features.weather_identification import WeatherIdentification
from sport_activities_features.tcx_manipulation import TCXFile

#read TCX file
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file("path_to_the_file")

#configure visual crossing api key
visual_crossing_api_key = "API_KEY" # https://www.visualcrossing.com/weather-api

#return weather objects
weather = WeatherIdentification(tcx_data['positions'], tcx_data['timestamps'], visual_crossing_api_key)
weatherlist = weather.get_weather()
```

### Using with Overpass queried Open Street Map nodes
```python
import overpy
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader

# External service Overpass API (https://wiki.openstreetmap.org/wiki/Overpass_API) (can be self hosted)
overpass_api = "https://lz4.overpass-api.de/api/interpreter"

# External service Open Elevation API (https://api.open-elevation.com/api/v1/lookup) (can be self hosted)
open_elevation_api = "https://api.open-elevation.com/api/v1/lookup"

# OSM Way (https://wiki.openstreetmap.org/wiki/Way)
open_street_map_way = 164477980

overpass_api = overpy.Overpass(url=overpass_api)

# Get an example Overpass way
q = f"""(way({open_street_map_way});<;);out geom;"""
query = overpass_api.query(q)

# Get nodes of an Overpass way
nodes = query.ways[0].get_nodes(resolve_missing=True)

# Extract basic data from nodes (you can later on use Hill Identification and Hill Data Extraction on them)
overpy_reader = OverpyNodesReader(open_elevation_api=open_elevation_api)
# Returns {
#         'positions': positions, 'altitudes': altitudes, 'distances': distances, 'total_distance': total_distance
#         }
data = overpy_reader.read_nodes(nodes)
```

### Extraction of data inside area
```python
import numpy as np
import sys
sys.path.append('../')

from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# Reading the TCX file.
tcx_file = TCXFile()
activity = tcx_file.read_one_file('path_to_the_data')

# Converting the read data to arrays.
positions = np.array([*activity['positions']])
distances = np.array([*activity['distances']])
timestamps = np.array([*activity['timestamps']])
heartrates = np.array([*activity['heartrates']])

# Area coordinates should be given in clockwise orientation in the form of 3D array (number_of_hulls, hull_coordinates, 2).
# Holes in area are permitted.
area_coordinates = np.array([[[10, 10], [10, 50], [50, 50], [50, 10]],
                             [[19, 19], [19, 21], [21, 21], [21, 19]]])

# Extracting the data inside the given area.
area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
area.identify_points_in_area()
area_data = area.extract_data_in_area()
```

## Datasets

Datasets are available on the following links: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip)

## Licence

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## Cite us

Fister Jr. I., Lukač L., Rajšp A., Fister I., Pečnik L., Fister D. A Minimalistic Toolbox for Extracting Features from Sport Activity Files. In: INES 2021, 2021.
