import pandas
from pymongo import MongoClient
from .core import read_mongo, to_mongo

pandas.DataFrame.to_mongo = to_mongo

__version__ = '0.0.0'
