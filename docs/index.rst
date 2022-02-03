sport-activities-features documentation!
========================================

.. automodule:: sport_activities_features

sport-activities-features is a minimalistic toolbox for extracting features from sport activity files written in Python.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/sport-activities-features
* **Python versions:** 3.6.x, 3.7.x, 3.8.x

General outline of the framework
-----------------------
Monitoring of sport activities produces many geographic, topologic and personalized data, with a vast majority of details hidden. Thus, a rigorous ex-post data analysis and statistic evaluation are required to extract them. Namely, most of the mainstream solutions for analyzing sport activities files rely on integral metrics, such as total duration, total distance and average hearth rate, which may suffer of "overall (integral) metrics problem". Among others, such problems are expressed in capturing sport activities in general only (ommiting crucial components), calculating potentially fallacious and misleading metrics, not recognizing different stages/phases of the sport activity (warm-up, endurance, intervals), and others.

The sport-activities-framework on the other side offers a detailed insight into the sport activity files. The framework supports both identification and extraction methods, such as identifying number of hills, extracting the average altitudes of identified hills, measuring total distance of identified hills, deriving climbing ratios (total distance of identified hills vs. total distance), average/total ascents of hills and so much more. The framework also integrates many other extensions, among others historical weather parsing, statistical evaluations and ex-post visualizations. Previous work on these topical questions were addressed in `relevant scientific papers on data mining <http://iztok-jr-fister.eu/static/publications/42.pdf>`_, also in a combination with the [generating/predicting automated sport training sessions](http://iztok-jr-fister.eu/static/publications/189.pdf).

Detailed insights
-----------------------
The sport-activities-features framework is compatible with TCX & GPX activity files and [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) nodes. Current version witholds (but is not limited to) following functions:
- extracting integral metrics, such as total distance, total duration, calories ([see example](examples/integral_metrics_extraction.py)),
- extracting topographic features, such as number of hills, average altitude of identified hills, total distance of identified hills, climbing ratio, average ascent of hills, total ascent, total descent ([see example](examples/hill_data_extraction.py)),
- plotting identified hills ([see example](examples/draw_map_with_identified_hills.py)),
- extracting the intervals, such as number of intervals, maximum/minimum/average duration of intervals, maximum/minimum/average distance of intervals, maximum/minimum/average heart rate during intervals,
- plotting the identified intervals ([see example](examples/draw_map_with_identified_intervals.py)),
- calculating the training loads, such as Bannister TRIMP, Lucia TRIMP([see example](examples/integral_metrics_extraction.py)),
- parsing the historical weather data from an external service,
- extracting the integral metrics of the activity inside area given with coordinates (distance, heartrate, speed) ([see example](examples/extract_data_inside_area.py)),
- extracting the activities from CSV file(s) and randomly selecting the specific number of activities ([see example](examples/extract_random_activities_from_csv.py)),
- extracting the dead ends,
- and much more.

The framework comes with two (testing) benchmark datasets, which are freely available to download from: [DATASET1](http://iztok-jr-fister.eu/static/publications/Sport5.zip), [DATASET2](http://iztok-jr-fister.eu/static/css/datasets/Sport.zip).

Historical Weather Data
-----------------------

Weather data parsed is collected from the [Visual Crossing Weather API](https://www.visualcrossing.com/).
Please note that this is an external unaffiliated service and users must register to use the API.
The service has a free tier (1000 Weather reports / day) but is otherwise operating on a pay-as-you-go model.
For pricing and terms of use please read the [official documentation](https://www.visualcrossing.com/weather-data-editions) of the API provider.

Documentation
=============

The main documentation is organized into a couple of sections:

* :ref:`user-docs`
* :ref:`dev-docs`
* :ref:`about-docs`

.. _user-docs:

.. toctree::
   :maxdepth: 3
   :caption: User Documentation

   getting_started

.. _dev-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   installation
   testing
   documentation
   api/index

.. _about-docs:

.. toctree::
   :maxdepth: 3
   :caption: About

   contributing
   code_of_conduct
