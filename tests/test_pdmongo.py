from unittest.mock import call

import pandas as pd
import pymongo
import pymongo.errors
import pytest

import pdmongo as pdm


def test_to_mongo_default_args(mocker):
    df = pd.DataFrame({'A': [1, 2]})
    collection_name = 'Acollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]
    pdm.to_mongo(df, collection_name, mock_db)
    mock_db[collection_name].insert_many.assert_called_with([{'A': 1}, {'A': 2}])


def test_to_mongo_with_index_true(mocker):
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]}).set_index('B')
    collection_name = 'Acollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]

    pdm.to_mongo(df, collection_name, mock_db)
    mock_db[collection_name].insert_many.assert_called_with([{'A': 1, 'B': 2}, {'A': 2, 'B': 3}])


def test_to_mongo_with_index_false(mocker):
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]}).set_index('B')
    collection_name = 'Acollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]

    pdm.to_mongo(df, collection_name, mock_db, index=False)
    mock_db[collection_name].insert_many.assert_called_with([{'A': 1}, {'A': 2}])


@pytest.mark.parametrize("chunksize, expected_calls", [
    (
        1,
        [call([{'A': 1}]), call([{'A': 2}]), call([{'A': 3}]), call([{'A': 4}])]
    ),
    (
        2,
        [call([{'A': 1}, {'A': 2}]), call([{'A': 3}, {'A': 4}])]
    ),
    (
        3,
        [call([{'A': 1}, {'A': 2}, {'A': 3}]), call([{'A': 4}])]
    ),
    (
        4,
        [call([{'A': 1}, {'A': 2}, {'A': 3}, {'A': 4}])]
    ),
])
def test_to_mongo_with_chunksize(chunksize, expected_calls, mocker):
    df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [2, 3, 4, 5]}).set_index('B')
    collection_name = 'Acollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]

    pdm.to_mongo(df, collection_name, mock_db, index=False, chunksize=chunksize)
    mock_db[collection_name].insert_many.assert_has_calls(expected_calls)


@pytest.mark.parametrize("chunksize", [
    3.2,
    'a',
    {},
    []
])
def test_to_mongo_with_chunksize_raises_type_error(chunksize, mocker):
    collection_name = 'ACollection'

    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]

    with pytest.raises(TypeError):
        pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, chunksize=chunksize)


@pytest.mark.parametrize("chunksize", [
    -1,
    -3
])
def test_to_mongo_with_chunksize_raises_value_error(chunksize, mocker):
    collection_name = 'ACollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]
    with pytest.raises(ValueError):
        pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, chunksize=chunksize)


def test_to_mongo_with_if_exists_fail_raises_value_error(mocker):
    collection_name = 'Acollection'
    mock_db = mocker.patch('pymongo.database.Database')
    with pytest.raises(ValueError, match='already exists'):
        pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, if_exists='fail')


def test_to_mongo_with_if_exists_replace_calls_drop(mocker):
    collection_name = 'ACollection'
    mock_db = mocker.patch('pymongo.database.Database')
    pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, if_exists='replace')
    mock_db[collection_name].drop.assert_called_once()


def test_to_mongo_with_if_exists_append(mocker):
    collection_name = 'ACollection'
    mock_db = mocker.patch('pymongo.database.Database')
    pdm.to_mongo(pd.DataFrame(), collection_name, mock_db, if_exists='append')
    mock_db[collection_name].drop.assert_not_called()


@pytest.mark.parametrize("if_exists", [
    "a",
    1,
    -1,
    {},
    []
])
def test_to_mongo_with_if_exists_invalid_raises_value_error(if_exists):
    collection_name = 'ACollection'
    with pytest.raises(ValueError):
        pdm.to_mongo(pd.DataFrame(), collection_name, {}, if_exists=if_exists)


def test_read_mongo(mocker):
    collection_name = 'ACollection'
    mock_db = mocker.patch('pymongo.database.Database')
    mock_db.validate_collection.side_effect = [pymongo.errors.OperationFailure("")]

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
