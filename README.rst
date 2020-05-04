========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-pandas-mongo/badge/?style=flat
    :target: https://readthedocs.org/projects/python-pandas-mongo
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/pakallis/python-pandas-mongo.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/pakallis/python-pandas-mongo

.. |coveralls| image:: https://coveralls.io/repos/pakallis/python-pandas-mongo/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/pakallis/python-pandas-mongo

.. |codecov| image:: https://codecov.io/gh/pakallis/python-pandas-mongo/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/pakallis/python-pandas-mongo

.. |version| image:: https://img.shields.io/pypi/v/pdmongo.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pdmongo

.. |wheel| image:: https://img.shields.io/pypi/wheel/pdmongo.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pdmongo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pdmongo.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pdmongo

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pdmongo.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pdmongo

.. |commits-since| image:: https://img.shields.io/github/commits-since/pakallis/python-pandas-mongo/vv0.0.2..svg
    :alt: Commits since latest release
    :target: https://github.com/pakallis/python-pandas-mongo/compare/vv0.0.2....master



.. end-badges

This package allows you to read/write pandas dataframes in MongoDB in the simplest way possible.

* Free software: MIT license

===========
Quick Start
===========

Writing a pandas DataFrame to a MongoDB collection::

	import pdmongo as pdm
	import pandas as pd

	df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
	df = pdm.read_mongo("MyCollection", [], "mongodb://localhost:27017/mydb")
	df.to_mongo(df, collection, uri)


Reading a MongoDB collection into a pandas DataFrame::

	import pdmongo as pdm
	df = pdm.read_mongo("MyCollection", [], "mongodb://localhost:27017/mydb")
	print(df)


============
Installation
============

::

    pip install pdmongo

You can also install the in-development version with::

    pip install https://github.com/pakallis/python-pandas-mongo/archive/master.zip


Documentation
=============


https://python-pandas-mongo.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
