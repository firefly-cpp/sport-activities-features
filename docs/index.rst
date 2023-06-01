sport-activities-features documentation!
========================================

.. automodule:: sport_activities_features

sport-activities-features is a minimalistic toolbox for extracting features from sports activity files written in Python.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/sport-activities-features
* **Python versions:** 3.6.x, 3.7.x, 3.8.x, 3.9.x, 3.10.x, 3.11.x

General outline of the framework
---------------------------------
Monitoring sports activities produce many geographic, topologic, and personalized data, with a vast majority of details hidden :cite:p:`rajvsp2020systematic`. Thus, a rigorous ex-post data analysis and statistic evaluation are required to extract them. Namely, most mainstream solutions for analyzing sports activities files rely on integral metrics, such as total duration, total distance, and average hearth rate, which may suffer from the "overall (integral) metrics problem". Among others, such problems are expressed in capturing sports activities in general only (omitting crucial components), calculating potentially fallacious and misleading metrics, not recognizing different stages/phases of the sports activity (warm-up, endurance, intervals), and others :cite:p:`fister2019computational`.

The sport-activities-framework, on the other side, offers a detailed insight into the sports activity files. The framework supports both identification and extraction methods, such as identifying the number of hills, extracting the average altitudes of identified hills, measuring the total distance of identified hills, deriving climbing ratios (total distance of identified hills vs. total distance), average/total ascents of hills and so much more. The framework also integrates many other extensions, among others, historical weather parsing, statistical evaluations, and ex-post visualizations. Previous work on these topical questions was addressed in :cite:p:`fister2013data` `relevant scientific papers on data mining <http://iztok-jr-fister.eu/static/publications/42.pdf>`_, also in combination with the `generating/predicting automated sport training sessions <http://iztok-jr-fister.eu/static/publications/189.pdf)>`_.

Detailed insights
-----------------------
The sport-activities-features framework is compatible with TCX & GPX activity files and `Overpass API <https://wiki.openstreetmap.org/wiki/Overpass_API>`_ nodes. Current version withholds (but is not limited to) the following functions:

- extracting integral metrics, such as total distance, total duration, calories (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/integral_metrics_extraction.py>`_),
- extracting topographic features, such as number of hills, the average altitude of identified hills, a total distance of identified hills, climbing ratio, the average ascent of hills, total ascent, total descent (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/hill_data_extraction.py>`_),
- plotting identified hills (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/draw_map_with_identified_hills.py>`_),
- extracting the intervals, such as number of intervals, maximum/minimum/average duration of intervals, maximum/minimum/average distance of intervals, maximum/minimum/average heart rate during intervals,
- plotting the identified intervals (`see example <.https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/draw_map_with_identified_intervals.py>`_),
- calculating the training loads, such as Bannister TRIMP, Lucia TRIMP (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/calculate_training_load.py>`_),
- parsing the historical weather data from an external service,
- extracting the integral metrics of the activity inside the area given with coordinates (distance, heartrate, speed) (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/extract_data_inside_area.py>`_),
- extracting the activities from CSV file(s) and randomly selecting the specific number of activities (`see example <../examples/extract_random_activities_from_csv.py>`_),
- extracting the dead ends (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/dead_end_extraction.py>`_),
- converting TCX to GPX (`see example <https://github.com/firefly-cpp/sport-activities-features/blob/main/examples/convert_tcx_to_gpx.py>`_),
- and much more.

The framework comes with two (testing) benchmark datasets, which are freely available to download from: `DATASET1 <http://iztok-jr-fister.eu/static/publications/Sport5.zip>`_, `DATASET2 <http://iztok-jr-fister.eu/static/css/datasets/Sport.zip>`_.

Historical Weather Data
-----------------------

Weather data is collected from the `Visual Crossing Weather API <https://www.visualcrossing.com/>`_.
Please note that this is an external unaffiliated service, and users must register to use the API.
The service has a free tier (1000 Weather reports/day) but otherwise operates on a pay-as-you-go model.
For pricing and terms of use, please read the `official documentation <https://www.visualcrossing.com/weather-data-editions>`_ of the API provider.

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
   contributors
   license

.. bibliography::
   :all:
