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

.. |commits-since| image:: https://img.shields.io/github/commits-since/pakallis/python-pandas-mongo/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/pakallis/python-pandas-mongo/compare/v0.0.0...master



.. end-badges

Transfer data between pandas dataframes and MongoDB

* Free software: MIT license

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
