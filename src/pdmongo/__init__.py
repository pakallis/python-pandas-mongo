import pandas
from .core import read_mongo, to_mongo

pandas.DataFrame.to_mongo = to_mongo

__version__ = '0.0.0'
