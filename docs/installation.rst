Installation
============

Setup development environment
-----------------------------

Requirements
~~~~~~~~~~~~

-  Poetry: https://python-poetry.org/docs/

After installing Poetry and cloning the project from GitHub, you should
run the following command from the root of the cloned project:

.. code:: sh

    $ poetry install

All of the project's dependencies should be installed and the project
ready for further development. **Note that Poetry creates a separate
virtual environment for your project.**

Development dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

List of sport-activities-features dependencies:

+----------------+--------------+------------+
| Package        | Version      | Platform   |
+================+==============+============+
| matplotlib     | ^3.3.3       | All        |
+----------------+--------------+------------+
| geopy          | ^2.0.0       | All        |
+----------------+--------------+------------+
| overpy         | >=0.6,<0.8   | All        |
+----------------+--------------+------------+
| geotiler       | ^0.15.1      | All        |
+----------------+--------------+------------+
| numpy          | >=1.26.4     | All        |
+----------------+--------------+------------+
| tcxreader      | ^0.4.11      | All        |
+----------------+--------------+------------+
| pandas         | >=2.0        | All        |
+----------------+--------------+------------+
| tcx2gpx        | 0.1.4        | All        |
+----------------+--------------+------------+
| gpxpy          | ^1.4.2       | All        |
+----------------+--------------+------------+
| setuptools     | <82          | All        |
+----------------+--------------+------------+

``setuptools`` is needed because geotiler 0.15.1 imports ``pkg_resources``,
which setuptools 82 removed. ``tcx2gpx`` stays at 0.1.4 because newer
versions cannot parse TCX timestamps ending in ``Z`` on Python 3.10.

List of development dependencies:

+----------------------+-----------+------------+
| Package              | Version   | Platform   |
+======================+===========+============+
| ruff                 | >=0.6     | Any        |
+----------------------+-----------+------------+
| pytest               | >=7.2.2   | Any        |
+----------------------+-----------+------------+
| Sphinx               | >=5.0.0   | Any        |
+----------------------+-----------+------------+
| sphinx-rtd-theme     | >=1.0.0   | Any        |
+----------------------+-----------+------------+
| sphinxcontrib-bibtex | ^2.4.1    | Any        |
+----------------------+-----------+------------+
