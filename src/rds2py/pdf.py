from typing import MutableMapping
import pandas as pd
from .parser import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def as_pandas_from_data_frame(robj: MutableMapping) -> pd.DataFrame:
    """Convert a realized R object to a Pandas `DataFrame` representation.

    Args:
        obj (MutableMapping): dict object parsed from the RDS file

    Raises:
        TypeError: `robj` is not a compatible class

    Returns:
        pd.DataFrame: a Pandas `DataFrame` representation of the R Object
    """

    cls = get_class(robj)

    if cls != "data.frame":
        raise TypeError(f"robj is not a `data.frame` but is `{cls}`")

    df = pd.DataFrame(
        robj["data"],
        columns=robj["attributes"]["names"]["data"],
        index=robj["attributes"]["row.names"]["data"],
    )

    return df


def as_pandas_from_dframe(robj: MutableMapping) -> pd.DataFrame:
    """Convert a realized R object to a pandas data frame representation

    Args:
        obj (MutableMapping): object parsed from the RDS file

    Raises:
        Exception: incorrect class

    Returns:
        pd.DataFrame: a Pandas `DataFrame` representation of the R Object
    """

    cls = get_class(robj)

    if cls != "DFrame":
        raise Exception(f"robj is not a `DFrame` but is `{cls}`")

    data = {}
    col_names = robj["attributes"]["listData"]["attributes"]["names"]["data"]
    for idx in range(len(col_names)):
        idx_asy = robj["attributes"]["listData"]["data"][idx]

        data[col_names[idx]] = idx_asy["data"]

    index = None
    if robj["attributes"]["rownames"]["data"]:
        index = robj["attributes"]["rownames"]["data"]

    df = pd.DataFrame(data, columns=col_names, index=index,)

    return df
