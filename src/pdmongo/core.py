from pandas import DataFrame


def read_mongo(
        collection,
        query,
        db,
        index_col=None,
        params=None,
        parse_dates=None,
        columns=None,
        chunksize=None):
    """
    Read MongoDB query into a DataFrame.

    Returns a DataFrame corresponding to the result set of the query. 
    Optionally provide an `index_col` parameter to use one of the
    columns as the index, otherwise default integer index will be used.

    Parameters
    ----------
    collection : str
        Mongo collection to select for querying
    query : list
        Must be an aggregate query.
        The input will be passed to pymongo `.aggregate` 
    db : pymongo.database.Database or database string URI
        The database to use
    index_col : str or list of str, optional, default: None
        Column(s) to set as index(MultiIndex).
    params : list, tuple or dict, optional, default: None
        List of parameters to pass to find/aggregate method.
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
          to the keyword arguments of :func:`pandas.to_datetime`
    chunksize : int, default None
        If specified, return an iterator where `chunksize` is the number of
        docs to include in each chunk.

    Returns
    -------
    Dataframe
    """
    return DataFrame.from_records(db[collection].aggregate(query))


def to_mongo(
    frame,
    name,
    db,
    schema=None,
    if_exists="fail",
    index=True,
    index_label=None,
    chunksize=None,
    dtype=None,
    method=None,
):
    """
    Write records stored in a DataFrame to a MongoDB collection.

    Parameters
    ----------
    frame : DataFrame, Series
    name : str
        Name of collection.
    db : pymongo.database.Database or database string URI
        The database to write to
    if_exists : {'fail', 'replace', 'append'}, default 'fail'
        - fail: If table exists, do nothing.
        - replace: If table exists, drop it, recreate it, and insert data.
        - append: If table exists, insert data. Create if does not exist.
    index : boolean, default True
        Write DataFrame index as a column.
    index_label : str or sequence, optional
        Column label for index column(s). If None is given (default) and
        `index` is True, then the index names are used.
        A sequence should be given if the DataFrame uses MultiIndex.
    chunksize : int, optional
        Specify the number of rows in each batch to be written at a time.
        By default, all rows will be written at once.
    dtype : dict or scalar, optional
        Specifying the datatype for columns. If a dictionary is used, the
        keys should be the column names and the values should be the
        MongoDB. If a scalar is provided, it will be applied to all columns.
    """
    records = frame.to_dict('records')
    if index is True:
        idx = frame.index
        idx_name = idx.name
        idx_data = idx.tolist()
        for i, record in enumerate(records):
            if index_label is None and idx_name is not None:
                record[idx_name] = idx_data[i]
    return db[name].insert_many(records)
