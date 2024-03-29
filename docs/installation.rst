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
| overpy         | ^0.6         | All        |
+----------------+--------------+------------+
| geotiler       | ^0.14.5      |  All       |
+----------------+--------------+------------+
| numpy          | \*           |  All       |
+----------------+--------------+------------+
| tcxreader      | ^0.4.4       | All        |
+----------------+--------------+------------+
| pandas         | \*           | All        |
+----------------+--------------+------------+
| niaaml         | ^1.2.0       | All        |
+----------------+--------------+------------+
| tcx2gpx        | 0.1.4        |  All       |
+----------------+--------------+------------+
| gpxpy          | 1.4.2        |  All       |
+----------------+--------------+------------+

List of development dependencies:

+----------------------+-----------+------------+
| Package              | Version   | Platform   |
+======================+===========+============+
| ruff                 | ^0.0.292  | Any        |
+----------------------+-----------+------------+
| pytest               | ^7.2.2    | Any        |
+----------------------+-----------+------------+
| coveralls            | ^2.2.0    | Any        |
+----------------------+-----------+------------+
| Sphinx               | ^5.0.0    | Any        |
+----------------------+-----------+------------+
| sphinx-rtd-theme     | ^1.0.0    | Any        |
+----------------------+-----------+------------+
| sphinxcontrib-bibtex | ^2.4.1    | Any        |
+----------------------+-----------+------------+