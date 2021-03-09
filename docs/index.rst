sport-activities-features documentation!
========================================

.. automodule:: sport_activities_features

sport-activities-features is a minimalistic toolbox for extracting features from sport activity files written in Python.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/sport-activities-features
* **Python versions:** 3.6.x, 3.7.x, 3.8.x

Objective
---------

Data analysis of sport activities that were monitored by the use of `sport trackers is popular <http://iztok-jr-fister.eu/static/publications/42.pdf>`_.
Many interesting utilizations of data are available, e.g. large-scale data mining of sport activities files for the `automatic sport training sessions generation <http://iztok-jr-fister.eu/static/publications/189.pdf>`_.

Most of the available solutions nowadays are relied upon integral metrics such as total duration, total distance, average hearth rate, etc. However,
such solutions may suffer of "overall (integral) metrics problem", commonly associated with following biases:

* details not expressed sufficiently,
* general/integral outlook of the race/training captured only,
* possibly fallacious intensity metrics of performed race/training and
* not recognized different stages/phases of the sport race/training, i.e. warming-up, endurance, intervals, etc.

Proposed software supports the extraction of following topographic features from sport activity files:

* number of hills,
* average altitude of identified hills,
* total distance of identified hills,
* climbing ratio (total distance of identified hills vs. total distance),
* average ascent of hills.

Full Features
-------------

* Extraction of integral metrics (total distance, total duration, calories).
* Extraction of topographic features (number of hills, average altitude of identified hills, total distance of identified hills, climbing ratio, average ascent of hills).
* Plotting the identified hills.
* Calculation of training loads (Bannister TRIMP, Lucia TRIMP).
* Parsing of Historical weather data from an external service.

Historical Weather Data
-----------------------

Weather data parsed is collected from the `Visual Crossing Weather API <https://www.visualcrossing.com/>`_. 
This is an external unaffiliated service and the user must register and use the API key provided from the service. 
The service has a free tier (1000 Weather reports / day) but is otherwise operating on a pay as you go model.
For the pricing and terms of use please read the `official documentation <https://www.visualcrossing.com/weather-data-editions>`_ of the API provider.

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
