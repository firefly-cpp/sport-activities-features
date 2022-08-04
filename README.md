<p align="center">
  <img width="200" src="https://raw.githubusercontent.com/firefly-cpp/sport-activities-features/main/.github/logo/sport_activities.png">
</p>

---

# sport-activities-features --- A minimalistic toolbox for extracting features from sports activity files written in Python

---

[![PyPI Version](https://img.shields.io/pypi/v/sport-activities-features.svg)](https://pypi.python.org/pypi/sport-activities-features)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sport-activities-features.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sport-activities-features.svg)
[![Downloads](https://pepy.tech/badge/sport-activities-features)](https://pepy.tech/project/sport-activities-features)
[![GitHub license](https://img.shields.io/github/license/firefly-cpp/sport-activities-features.svg)](https://github.com/firefly-cpp/sport-activities-features/blob/master/LICENSE)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/sport-activities-features.svg)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/sport-activities-features.svg)](http://isitmaintained.com/project/firefly-cpp/sport-activities-features "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/sport-activities-features.svg)](http://isitmaintained.com/project/firefly-cpp/sport-activities-features "Percentage of issues still open")
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
[![Fedora package](https://img.shields.io/fedora/v/python3-sport-activities-features?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-sport-activities-features)
[![AUR package](https://img.shields.io/aur/version/python-sport-activities-features?color=blue&label=Arch%20Linux&logo=arch-linux)](https://aur.archlinux.org/packages/python-sport-activities-features)
[![DOI](https://img.shields.io/badge/DOI-10.1109/INES52918.2021.9512927-blue)](https://doi.org/10.1109/INES52918.2021.9512927)

## General outline of the framework
Monitoring sports activities produce many geographic, topologic, and personalized data, with a vast majority of details hidden. Thus, a rigorous ex-post data analysis and statistic evaluation are required to extract them. Namely, most mainstream solutions for analyzing sports activities files rely on integral metrics, such as total duration, total distance, and average heart rate, which may suffer from the "overall (integral) metrics problem." Among others, such problems are expressed in capturing sports activities in general only (omitting crucial components), calculating potentially fallacious and misleading metrics, not recognizing different stages/phases of the sports activity (warm-up, endurance, intervals), and others.

The sport-activities-framework, on the other side, offers a detailed insight into the sports activity files. The framework supports both identification and extraction methods, such as identifying the number of hills, extracting the average altitudes of identified hills, measuring the total distance of identified hills, deriving climbing ratios (total distance of identified hills vs. total distance), average/total ascents of hills and so much more. The framework also integrates many other extensions, among others, historical weather parsing, statistical evaluations, and ex-post visualizations. Previous work on these topical questions was addressed in [relevant scientific papers on data mining](http://iztok-jr-fister.eu/static/publications/42.pdf), also in combination with the [generating/predicting automated sport training sessions](http://iztok-jr-fister.eu/static/publications/189.pdf).


## Detailed insights
The sport-activities-features framework is compatible with TCX & GPX activity files and [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) nodes. The current version withholds (but is not limited to) the following functions:
- extracting integral metrics, such as total distance, total duration, calories ([see example](examples/integral_metrics_extraction.py)),
- extracting topographic features, such as the number of hills, the average altitude of identified hills, the total distance of identified hills, climbing ratio, average ascent of hills, total ascent, and total descent ([see example](examples/hill_data_extraction.py)),
- plotting identified hills ([see example](examples/draw_map_with_identified_hills.py)),
- extracting the intervals, such as number of intervals, maximum/minimum/average duration of intervals, maximum/minimum/average distance of intervals, maximum/minimum/average heart rate during intervals,
- plotting the identified intervals ([see example](examples/draw_map_with_identified_intervals.py)),
- calculating the training loads, such as Banister TRIMP, Lucia TRIMP([see example](examples/calculate_training_load.py)),
- parsing the historical weather data from an external service,
- extracting the integral metrics of the activity inside the area given with coordinates (distance, heart rate, speed) ([see example](examples/extract_data_inside_area.py)),
- extracting the activities from CSV file(s) and randomly selecting the specific number of activities ([see example](examples/extract_random_activities_from_csv.py)),
- extracting the dead ends,
- and much more.

The framework comes with two (testing) benchmark datasets, which are freely available to download from: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip).


## Installation

### pip3

Install sport-activities-features with pip3:

```sh
pip3 install sport-activities-features
```

### Alpine Linux

To install sport-activities-features on Alpine, use:

```sh
$ apk add py3-sport-activities-features
```

### Fedora Linux

To install sport-activities-features on Fedora, use:

```sh
$ dnf install python3-sport-activities-features
```

### Arch Linux

To install sport-activities-features on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):

```sh
$ yay -Syyu python-sport-activities-features
```

## API

There is a simple API for remote work with the sport-activities-features package available [here](https://github.com/alenrajsp/sport-activities-features-api).


## Historical weather data
Weather data parsed is collected from the [Visual Crossing Weather API](https://www.visualcrossing.com/).
Please note that this is an external unaffiliated service, and users must register to use the API.
The service has a free tier (1000 Weather reports/day) but is otherwise operating on a pay-as-you-go model.
For pricing and terms of use, please read the [official documentation](https://www.visualcrossing.com/weather-data-editions) of the API provider.

## Overpass API & Open Elevation API integration
Without performing activities, we can use the [OpenStreetMap](https://www.openstreetmap.org/) for the identification of hills,
total ascent, and descent. This is done using the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)
which is a read-only API that allows querying of OSM map data. In addition to that altitude, data is retrieved by using the
[Open-Elevation API](https://open-elevation.com/) which is an open-source and free alternative to the Google Elevation API.
Both of the solutions can be used by using free publicly acessible APIs ([Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API), [Open-Elevation](https://open-elevation.com/#public-api)) or can be self hosted on a server or as a Docker container ([Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API/Installation), [Open-Elevation](https://github.com/Jorl17/open-elevation/blob/master/docs/host-your-own.md)).

## CODE EXAMPLES:

### Reading files

#### (*.TCX)
```python
from sport_activities_features.tcx_manipulation import TCXFile

# Class for reading TCX files
tcx_file=TCXFile()
data = tcx_file.read_one_file("path_to_the_file") # Represents data as dictionary of lists

# Alternative choice
data = tcx_file.read_one_file("path_to_the_file", numpy_array= True) # Represents data as dictionary of numpy.arrays

```

#### (*.GPX)
```python
from sport_activities_features.gpx_manipulation import GPXFile

# Class for reading GPX files
gpx_file=GPXFile()

# Read the file and generate a dictionary with 
data = gpx_file.read_one_file("path_to_the_file") # Represents data as dictionary of lists

# Alternative choice
data = gpx_file.read_one_file("path_to_the_file", numpy_array= True) # Represents data as dictionary of numpy.arrays

```



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

### Parsing of Historical weather data from an external service
```python
from sport_activities_features import WeatherIdentification
from sport_activities_features import TCXFile

# Read TCX file
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file("path_to_file")

# Configure visual crossing api key
visual_crossing_api_key = "weather_api_key" # https://www.visualcrossing.com/weather-api

# Explanation of elements - https://www.visualcrossing.com/resources/documentation/weather-data/weather-data-documentation/
weather = WeatherIdentification(tcx_data['positions'], tcx_data['timestamps'], visual_crossing_api_key)
weatherlist = weather.get_weather(time_delta=30)
tcx_weather = weather.get_average_weather_data(timestamps=tcx_data['timestamps'],weather=weatherlist)
# Add weather to TCX data
tcx_data.update({'weather':tcx_weather})
```

The weather list is of the following type:
```json
     [
        {
            "temperature": 14.3,
            "maximum_temperature": 14.3,
            "minimum_temperature": 14.3,
            "wind_chill": null,
            "heat_index": null,
            "solar_radiation": null,
            "precipitation": 0.0,
            "sea_level_pressure": 1021.6,
            "snow_depth": null,
            "wind_speed": 6.9,
            "wind_direction": 129.0,
            "wind_gust": null,
            "visibility": 40.0,
            "cloud_cover": 54.3,
            "relative_humidity": 47.6,
            "dew_point": 3.3,
            "weather_type": "",
            "conditions": "Partially cloudy",
            "date": "2016-04-02T17:26:09+00:00",
            "location": [
                46.079871179535985,
                14.738618675619364
            ],
            "index": 0
        }, ...
    ]
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

### Using Overpass queried Open Street Map nodes
```python
import overpy
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader

# External service Overpass API (https://wiki.openstreetmap.org/wiki/Overpass_API) (can be self-hosted)
overpass_api = "https://lz4.overpass-api.de/api/interpreter"

# External service Open Elevation API (https://api.open-elevation.com/api/v1/lookup) (can be self-hosted)
open_elevation_api = "https://api.open-elevation.com/api/v1/lookup"

# OSM Way (https://wiki.openstreetmap.org/wiki/Way)
open_street_map_way = 164477980

overpass_api = overpy.Overpass(url=overpass_api)

# Get an example Overpass way
q = f"""(way({open_street_map_way});<;);out geom;"""
query = overpass_api.query(q)

# Get nodes of an Overpass way
nodes = query.ways[0].get_nodes(resolve_missing=True)

# Extract basic data from nodes (you can, later on, use Hill Identification and Hill Data Extraction on them)
overpy_reader = OverpyNodesReader(open_elevation_api=open_elevation_api)
# Returns {
#         'positions': positions, 'altitudes': altitudes, 'distances': distances, 'total_distance': total_distance
#         }
data = overpy_reader.read_nodes(nodes)
```

### Extraction of data inside the area
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

### Identify interruptions
```python
from sport_activities_features.interruptions.interruption_processor import InterruptionProcessor
from sport_activities_features.tcx_manipulation import TCXFile

"""
Identify interruption events from a TCX or GPX file.
"""

# read TCX file (also works with GPX files)
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file("path_to_the_data")

"""
Time interval = time before and after the start of an event
Min speed = Threshold speed to trigger an event/interruption (trigger when under min_speed)
overpass_api_url = Set to something self-hosted, or use a public instance from https://wiki.openstreetmap.org/wiki/Overpass_API
"""
interruptionProcessor = InterruptionProcessor(time_interval=60, min_speed=2,
                                              overpass_api_url="url_to_overpass_api")

"""
If classify is set to true, also discover if interruptions are close to intersections. Returns a list of [ExerciseEvent]
"""
events = interruptionProcessor.events(tcx_data, True)
```

### Overpy (Overpass API) node manipulation
Generate TCXFile parsed like data object from overpy.Node objects
```python
import overpy
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader


# External service Overpass API (https://wiki.openstreetmap.org/wiki/Overpass_API) (can be self-hosted)
overpass_api = "https://lz4.overpass-api.de/api/interpreter"

# External service Open Elevation API (https://api.open-elevation.com/api/v1/lookup) (can be self-hosted)
open_elevation_api = "https://api.open-elevation.com/api/v1/lookup"

# OSM Way (https://wiki.openstreetmap.org/wiki/Way)
open_street_map_way = 164477980

overpass_api = overpy.Overpass(url=overpass_api)

# Get an example Overpass way
q = f"""(way({open_street_map_way});<;);out geom;"""
query = overpass_api.query(q)

# Get nodes of an Overpass way
nodes = query.ways[0].get_nodes(resolve_missing=True)

# Extract basic data from nodes (you can, later on, use Hill Identification and Hill Data Extraction on them)
overpy_reader = OverpyNodesReader(open_elevation_api=open_elevation_api)
# Returns {
#         'positions': positions, 'altitudes': altitudes, 'distances': distances, 'total_distance': total_distance
#         }
data = overpy_reader.read_nodes(nodes)
```
### Missing elevation data extraction
```python
from sport_activities_features import ElevationIdentification
from sport_activities_features import TCXFile

tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file('path_to_file')

elevations = ElevationIdentification(tcx_data['positions'])
"""Adds tcx_data['elevation'] = eg. [124, 21, 412] for each position"""
tcx_data.update({'elevations':elevations})
```

### Example of a visualization of the area detection

![Area Figure](https://i.imgur.com/Iz8Ga3B.png)

### Example of visualization of dead-end identification
![Dead End Figure](https://imgur.com/LgZzCFS.png)

## License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## Cite us

I. Jr. Fister, L. Lukač, A. Rajšp, I. Fister, L. Pečnik and D. Fister, "[A minimalistic toolbox for extracting features from sport activity files](http://iztok-jr-fister.eu/static/publications/294.pdf)", 2021 IEEE 25th International Conference on Intelligent Engineering Systems (INES), 2021, pp. 121-126, doi: [10.1109/INES52918.2021.9512927](http://dx.doi.org/10.1109/INES52918.2021.9512927).

## Contributors ✨

Thanks go to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://www.iztok-jr-fister.eu/"><img src="https://avatars.githubusercontent.com/u/1633361?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Iztok Fister Jr.</b></sub></a><br /><a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=firefly-cpp" title="Code">💻</a> <a href="https://github.com/firefly-cpp/sport-activities-features/issues?q=author%3Afirefly-cpp" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=firefly-cpp" title="Tests">⚠️</a> <a href="#example-firefly-cpp" title="Examples">💡</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=firefly-cpp" title="Documentation">📖</a> <a href="#ideas-firefly-cpp" title="Ideas, Planning, & Feedback">🤔</a> <a href="#mentoring-firefly-cpp" title="Mentoring">🧑‍🏫</a> <a href="#platform-firefly-cpp" title="Packaging/porting to new platform">📦</a> <a href="#maintenance-firefly-cpp" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/alenrajsp"><img src="https://avatars.githubusercontent.com/u/27721714?v=4?s=100" width="100px;" alt=""/><br /><sub><b>alenrajsp</b></sub></a><br /><a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=alenrajsp" title="Code">💻</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=alenrajsp" title="Tests">⚠️</a> <a href="#example-alenrajsp" title="Examples">💡</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=alenrajsp" title="Documentation">📖</a> <a href="#ideas-alenrajsp" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/firefly-cpp/sport-activities-features/issues?q=author%3Aalenrajsp" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/luckyLukac"><img src="https://avatars.githubusercontent.com/u/73126820?v=4?s=100" width="100px;" alt=""/><br /><sub><b>luckyLukac</b></sub></a><br /><a href="#ideas-luckyLukac" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=luckyLukac" title="Code">💻</a> <a href="https://github.com/firefly-cpp/sport-activities-features/issues?q=author%3AluckyLukac" title="Bug reports">🐛</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=luckyLukac" title="Tests">⚠️</a> <a href="#example-luckyLukac" title="Examples">💡</a></td>
    <td align="center"><a href="https://github.com/rhododendrom"><img src="https://avatars.githubusercontent.com/u/3198785?v=4?s=100" width="100px;" alt=""/><br /><sub><b>rhododendrom</b></sub></a><br /><a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=rhododendrom" title="Code">💻</a> <a href="#design-rhododendrom" title="Design">🎨</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=rhododendrom" title="Documentation">📖</a> <a href="#ideas-rhododendrom" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/lukapecnik"><img src="https://avatars.githubusercontent.com/u/23029992?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Luka Pečnik</b></sub></a><br /><a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=lukapecnik" title="Code">💻</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=lukapecnik" title="Documentation">📖</a> <a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=lukapecnik" title="Tests">⚠️</a> <a href="https://github.com/firefly-cpp/sport-activities-features/issues?q=author%3Alukapecnik" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/spelap"><img src="https://avatars.githubusercontent.com/u/19300429?v=4?s=100" width="100px;" alt=""/><br /><sub><b>spelap</b></sub></a><br /><a href="https://github.com/firefly-cpp/sport-activities-features/commits?author=spelap" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!
