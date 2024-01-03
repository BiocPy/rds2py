from .parser import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def as_pandas_from_data_frame(robj):
    """Read an R object to a :py:class:`~pandas.DataFrame`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from pandas import DataFrame

    cls = get_class(robj)

    if cls != "data.frame":
        raise TypeError("`robj` does not contain a 'data.frame'.")

    df = DataFrame(
        robj["data"],
        columns=robj["attributes"]["names"]["data"],
        index=robj["attributes"]["row.names"]["data"],
    )

    return df


def as_pandas_from_dframe(robj):
    """Convert a realized R object to a pandas data frame representation.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from pandas import DataFrame

    cls = get_class(robj)

    if cls != "DFrame":
        raise Exception("`robj` does not contain a 'DFrame'.")

    data = {}
    col_names = robj["attributes"]["listData"]["attributes"]["names"]["data"]
    for idx in range(len(col_names)):
        idx_asy = robj["attributes"]["listData"]["data"][idx]

        data[col_names[idx]] = idx_asy["data"]

    index = None
    if robj["attributes"]["rownames"]["data"]:
        index = robj["attributes"]["rownames"]["data"]

    df = DataFrame(
        data,
        columns=col_names,
        index=index,
    )

    return df
