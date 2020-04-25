import pandas as pd
import pytest

import pdmongo as pdm


def test_to_mongo_default_args(mocker):
    df = pd.DataFrame({'A': [1, 2]})

    class DBStub():
        def insert_many(self, docs):
            pass

    collection_name = 'Acollection'
    db = {collection_name: DBStub()}
    spy = mocker.spy(db[collection_name], 'insert_many')

    pdm.to_mongo(df, collection_name, db)
    spy.assert_called_with([{'A': 1}, {'A': 2}])


def test_to_mongo_with_index_true(mocker):
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]}).set_index('B')

    class DBStub():
        def insert_many(self, docs):
            pass

    collection_name = 'Acollection'
    db = {collection_name: DBStub()}
    spy = mocker.spy(db[collection_name], 'insert_many')

    pdm.to_mongo(df, collection_name, db)
    spy.assert_called_with([{'A': 1, 'B': 2}, {'A': 2, 'B': 3}])


def test_to_mongo_with_index_false(mocker):
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]}).set_index('B')

    class DBStub():
        def insert_many(self, docs):
            pass

    collection_name = 'Acollection'
    db = {collection_name: DBStub()}
    spy = mocker.spy(db[collection_name], 'insert_many')

    pdm.to_mongo(df, collection_name, db, index=False)
    spy.assert_called_with([{'A': 1}, {'A': 2}])


def test_read_mongo(mocker):
    class DBStub():
        def aggregate(self, docs):
            return []

    collection_name = 'ACollection'
    db = {collection_name: DBStub()}
    mock = mocker.spy(db[collection_name], 'aggregate')
    pdm.read_mongo(collection_name, [], db)
    mock.assert_called_with([])


def test_read_mongo_chunksize(mocker):
    class DBStub():
        def aggregate(self, docs, **kwargs):
            return []

    collection_name = 'ACollection'
    batch_size = 2
    db = {collection_name: DBStub()}
    mock = mocker.spy(db[collection_name], 'aggregate')
    pdm.read_mongo(collection_name, [], db, chunksize=batch_size)
    mock.assert_called_with([], batchSize=batch_size)


def test_read_mongo_index_col(mocker):
    class DBStub():
        def aggregate(self, docs, **kwargs):
            return [
                {
                    't': '2020-01-01T00:00:00.000Z', 'v': 20
                },
                {
                    't': '2020-01-01T01:00:00.000Z', 'v': 15
                }
            ]

    collection_name = 'ACollection'
    db = {collection_name: DBStub()}
    df = pdm.read_mongo(collection_name, [], db, index_col='t')
    assert df.index[0] == '2020-01-01T00:00:00.000Z'
    assert df.v[0] == 20


def test_read_mongo_index_col_multi_index(mocker):
    class DBStub():
        def aggregate(self, docs, **kwargs):
            return [
                {
                    't': '2020-01-01T00:00:00.000Z', 'v': 20
                },
                {
                    't': '2020-01-01T01:00:00.000Z', 'v': 15
                }
            ]

    collection_name = 'ACollection'
    db = {collection_name: DBStub()}
    df = pdm.read_mongo(collection_name, [], db, index_col=['t', 'v'])
    assert df.index[0][0] == '2020-01-01T00:00:00.000Z'
    assert df.index[0][1] == 20
    assert not df.values.size > 0


def test_read_mongo_db_str(mocker):
    class CollectionStub():
        def aggregate(self, query, **kwargs):
            return [
                {
                    't': '2020-01-01T00:00:00.000Z', 'v': 20
                },
                {
                    't': '2020-01-01T01:00:00.000Z', 'v': 15
                }
            ]

    class DBStub:
        def __getitem__(self, item):
            return CollectionStub()

    mock = mocker.patch("pymongo.database.Database")
    mock.return_value = DBStub()
    collection_name = 'ACollection'

    db_uri = "mongodb://localhost:27017/pd-mongo-sample-db"
    df = pdm.read_mongo(collection_name, [], db_uri)
    assert df.index[0] == 0
    assert df.values[0][0] == '2020-01-01T00:00:00.000Z'
    assert not df.values.size == 2


def test_read_mongo_params(mocker):
    collection_name = 'ACollection'

    class CollectionStub:
        def aggregate(self, docs, **kwargs):
            pass

    collection_mock = mocker.Mock(CollectionStub)
    collection_mock.aggregate.return_value = []
    db = {collection_name: collection_mock}
    pdm.read_mongo(collection_name, [], db, extra={'allowDiskUse': True})
    collection_mock.aggregate.assert_called_with([], allowDiskUse=True)


def test_read_mongo_params_batch_size_and_chunksize_raises_value_error(mocker):
    collection_name = 'ACollection'

    class CollectionStub:
        def aggregate(self, docs, **kwargs):
            pass

    collection_mock = mocker.Mock(CollectionStub)
    collection_mock.aggregate.return_value = []
    db = {collection_name: collection_mock}
    with pytest.raises(ValueError):
        pdm.read_mongo(collection_name, [], db, chunksize=30, extra={'batchSize': 20})
