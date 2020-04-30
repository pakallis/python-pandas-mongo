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


=================================================
Reading dataframes from MongoDB using aggregation
=================================================

You can use an aggregation query to filter/transform data in MongoDB before fetching them into a data frame.

Reading a collection from MongoDB into a pandas DataFrame by using an aggregation query::

	import pdmongo as pdm
    query = [ 
		{
			"$match": {
				'A': 1
			}
		}
	]
	df = pdm.read_mongo("MyCollection", query, "mongodb://localhost:27017/mydb")
	print(df)

The *query* accepts the same arguments as method *aggregate* of pymongo package.