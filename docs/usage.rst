=====
Usage
=====

Writing a pandas DataFrame to a MongoDB collection::

	import pdmongo as pdm
	import pandas as pd

	df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
	uri = "mongodb://localhost:27017/mydb"
	collection = "ACollection"
	aggregation_query = []
	df = pdm.read_mongo(collection, aggregation_query, uri)
	df.to_mongo(df, collection, uri)


Reading data from MongoDB into a pandas DataFrame::

	import pdmongo as pdm
	uri = "mongodb://localhost:27017/mydb"
	collection = "ACollection"
	aggregation_query = []
	df = pdm.read_mongo(collection, aggregation_query, uri)
	print(df)