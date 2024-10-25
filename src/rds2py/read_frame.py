"""Functions for parsing R data frame objects.

This module provides parsers for converting both base R `data.frame` objects
and Bioconductor `DataFrame` objects into Python `BiocFrame` objects, preserving
row names, column names, and data types.
"""

from biocframe import BiocFrame

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_data_frame(robject: dict, **kwargs):
    """Convert an R data.frame to a :py:class:`~biocframe.BiocFrame` object.

    Args:
        robject:
            Dictionary containing parsed R `data.frame` object.

        **kwargs:
            Additional arguments.

    Returns:
        A BiocFrame object containing the data frame's contents,
        with preserved column and row names.
    """
    cls = get_class(robject)

    if cls != "data.frame":
        raise RuntimeError("`robject` does not contain a 'data.frame'.")

    col_names = _dispatcher(robject["attributes"]["names"], **kwargs)

    bframe_obj = {}
    for idx, rd in enumerate(robject["data"]):
        bframe_obj[col_names[idx]] = _dispatcher(rd, **kwargs)

    df = BiocFrame(
        bframe_obj,
        row_names=_dispatcher(robject["attributes"]["row.names"], **kwargs),
    )

    return df


def read_dframe(robject: dict, **kwargs):
    """Convert an R DFrame (Bioconductor's `DataFrame`) to a `BiocFrame` object.

    Args:
        robject:
            Dictionary containing parsed R `DFrame` object.

        **kwargs:
            Additional arguments.

    Returns:
        A BiocFrame object containing the DataFrame's contents,
        with preserved metadata and structure.
    """
    from biocframe import BiocFrame

    cls = get_class(robject)

    if cls != "DFrame":
        raise RuntimeError("`robject` does not contain a 'DFrame'.")

    data = {}
    col_names = _dispatcher(robject["attributes"]["listData"]["attributes"]["names"], **kwargs)
    for idx, colname in enumerate(col_names):
        data[colname] = _dispatcher(robject["attributes"]["listData"]["data"][idx], **kwargs)

    index = None
    if robject["attributes"]["rownames"]["data"]:
        index = _dispatcher(robject["attributes"]["rownames"], **kwargs)

    nrows = None
    if robject["attributes"]["nrows"]["data"]:
        nrows = list(_dispatcher(robject["attributes"]["nrows"]), **kwargs)[0]

    df = BiocFrame(
        data,
        # column_names=col_names,
        row_names=index,
        number_of_rows=nrows,
    )

    return df
