# sport-activities-features --- A minimalistic toolbox for extracting features from sport activity files written in Python

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
- average ascent of hills.


## Installation

```sh
pip install sport-activities-features
```

## Full Features

- Extraction of integral metrics (total distance, total duration, calories) ([see example](examples/integral_metrics_extraction.py))
- Extraction of topographic features (number of hills, average altitude of identified hills, total distance of identified hills, climbing ratio, average ascent of hills) ([see example](examples/hill_data_extraction.py))
- Plotting the identified hills ([see example](examples/draw_map_with_identified_hills.py)) 
- Calculation of training loads (Bannister TRIMP, Lucia TRIMP) ([see example](examples/integral_metrics_extraction.py))
- Parsing of Historical weather data from an external service

## Historical weather data
Weather data parsed is collected from the [Visual Crossing Weather API](https://www.visualcrossing.com/). 
This is an external unaffiliated service and the user must register and use the API key provided from the service. 
The service has a free tier (1000 Weather reports / day) but is otherwise operating on a pay as you go model.
For the pricing and terms of use please read the [official documentation](https://www.visualcrossing.com/weather-data-editions) of the API provider.

## CODE EXAMPLES:

### Extraction of topographic features
```python
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.plot_data import PlotData

#read TCX file
tcx_file = TCXFile()
activity = tcx_file.read_one_file("path_to_the_file")

#detect hills in data
Hill = HillIdentification(activity['altitudes'], 30)
Hill.identify_hills()
all_hills = Hill.return_hills()

#extract features from data
Top = TopographicFeatures(all_hills)
num_hills = Top.num_of_hills()
avg_altitude = Top.avg_altitude_of_hills(activity['altitudes'])
avg_ascent = Top.avg_ascent_of_hills(activity['altitudes'])
distance_hills = Top.distance_of_hills(activity['positions'])
hills_share = Top.share_of_hills(distance_hills, activity['total_distance'])
```

### Extraction of integral metrics
```python
import sys
sys.path.append('../')

from sport_activities_features.tcx_manipulation import TCXFile

#read TCX file
tcx_file = TCXFile()

integral_metrics = tcx_file.extract_integral_metrics("path_to_the_file")

print(integral_metrics)

```
## Datasets

Datasets are available on the following links: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip)

## Licence

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
