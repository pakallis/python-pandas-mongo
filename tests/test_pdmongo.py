import pandas as pd
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
    df = pd.DataFrame({'A': [1, 2], 'B': [2,3]}).set_index('B')
    class DBStub():
        def insert_many(self, docs):
            pass

    collection_name = 'Acollection'
    db = {collection_name: DBStub()}
    spy = mocker.spy(db[collection_name], 'insert_many')

    pdm.to_mongo(df, collection_name, db)
    spy.assert_called_with([{'A': 1, 'B': 2}, {'A': 2, 'B': 3}])


def test_to_mongo_with_index_false(mocker):
    df = pd.DataFrame({'A': [1, 2], 'B': [2,3]}).set_index('B')
    class DBStub():
        def insert_many(self, docs):
            pass

    collection_name = 'Acollection'
    db = {collection_name: DBStub()}
    spy = mocker.spy(db[collection_name], 'insert_many')

    pdm.to_mongo(df, collection_name, db, index=False)
    spy.assert_called_with([{'A': 1}, {'A': 2}])