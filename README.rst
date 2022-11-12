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

.. |commits-since| image:: https://img.shields.io/github/commits-since/pakallis/python-pandas-mongo/v0.2.3.svg
    :alt: Commits since latest release
    :target: https://github.com/pakallis/python-pandas-mongo/compare/v0.2.3...master



.. end-badges

This package allows you to read/write pandas dataframes in MongoDB in the simplest way possible.

* Free software: MIT license

===========
Quick Start
===========

Install pdmongo::

    pip install pdmongo

Write a pandas DataFrame to a MongoDB collection::

    import pandas as pd
    import pdmongo as pdm

    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df.to_mongo("MyCollection", "mongodb://localhost:27017/mydb")

Read a MongoDB collection into a pandas DataFrame::

    import pdmongo as pdm

    df = pdm.read_mongo("MyCollection", [], "mongodb://localhost:27017/mydb")
    print(df)



====================
Examples / use cases
====================

Reading a MongoDB collection into a pandas data frame (aggregation query)
=========================================================================

You can use an aggregation query to filter/transform data in MongoDB before fetching them into a data frame.
This allows you to delegate the slow operation to MongoDB.

Reading a collection from MongoDB into a pandas DataFrame by using an aggregation query::

    import pdmongo as pdm
    import pandas as pd

    # First generate some data and write them to MongoDB
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df.to_mongo(df, 'MyCollection', "mongodb://localhost:27017/mydb")

    # Filter with an aggregate query and parse results into a data frame.
    query = [{"$match": {'A': 1} }]
    df = pdm.read_mongo("MyCollection", query, "mongodb://localhost:27017/mydb")
    print(df) # Only values where A > 1 is returned

The *query* accepts the same arguments as the *aggregate* method of pymongo package.



Write MongoDB to a PostgreSQL table
===================================

You can write a MongoDB collection to a PostgreSQL table::

    import numpy as np
    import pandas as pd
    import pdmongo as pdm
    from sqlalchemy import create_engine

    # Generate some data and write them to MongoDB
    df = pd.DataFrame({'A': [1, 2, 3]})
    df.to_mongo("MyCollection", "mongodb://localhost:27017/mydb")

    # Read data from MongoDB and write them to PostgreSQL
    new_df = pdm.read_mongo("MyCollection", [], "mongodb://localhost:27017/mydb")
    engine = create_engine('postgres://postgres:postgres@localhost:5432', echo=False)
    new_df[["A"]].to_sql("APostgresTable", engine)


Plot data retrieved from a MongoDB Collection
=============================================

You can plot a collection retrieved from MongoDB

::

    import numpy as np
    import pandas as pd
    import pdmongo as pdm
    import matplotlib.pyplot as plt

    # Generate data and write them to MongoDB
    df = pd.DataFrame({'Value': np.random.randn(1000)})
    df.to_mongo('TimeSeries', 'mongodb://localhost:27017/mydb')

    # Read collection from MongoDB and plot data
    new_df = pdm.read_mongo("TimeSeries", [], "mongodb://localhost:27017/mydb")
    new_df.plot()
    plt.show()


============
Installation
============

::

    pip install pdmongo

You can also install the in-development version with::

    pip install https://github.com/pakallis/python-pandas-mongo/archive/master.zip


=============
Documentation
=============

You can find the documentation at::

    https://python-pandas-mongo.readthedocs.io/

===========
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
