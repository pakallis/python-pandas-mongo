import pandas

from .core import read_mongo  # noqa
from .core import to_mongo

pandas.DataFrame.to_mongo = to_mongo

__all__ = ['read_mongo', 'to_mongo']
__version__ = '0.1.0'
