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
| geopy          | ^2.0.0       | All        |
+----------------+--------------+------------+
| matplotlib     | ^3.3.3       | All        |
+----------------+--------------+------------+
| tcxreader      | ^0.3.0       | All        |
+----------------+--------------+------------+
| requests       | ^2.25.1      | All        |
+----------------+--------------+------------+
| niaaml         | ^1.1.0       | All        |
+----------------+--------------+------------+

List of development dependencies:

+--------------------+-----------+------------+
| Package            | Version   | Platform   |
+====================+===========+============+
| Sphinx             | ^3.5.1    | Any        |
+--------------------+-----------+------------+
| sphinx-rtd-theme   | ^0.5.1    | Any        |
+--------------------+-----------+------------+