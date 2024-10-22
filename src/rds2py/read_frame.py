from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_data_frame(robject: dict):
    """Read an R object to a :py:class:`~biocframe.BiocFrame`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from biocframe import BiocFrame

    cls = get_class(robject)

    if cls != "data.frame":
        raise RuntimeError("`robject` does not contain a 'data.frame'.")

    col_names = _dispatcher(robject["attributes"]["names"])

    bframe_obj = {}
    for idx, rd in enumerate(robject["data"]):
        bframe_obj[col_names[idx]] = _dispatcher(rd)

    df = BiocFrame(
        bframe_obj,
        row_names=_dispatcher(robject["attributes"]["row.names"]),
    )

    return df


def parse_dframe(robject: dict):
    """Convert a realized R object to a pandas data frame representation.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from biocframe import BiocFrame

    cls = get_class(robject)

    if cls != "DFrame":
        raise RuntimeError("`robject` does not contain a 'DFrame'.")

    data = {}
    col_names = _dispatcher(robject["attributes"]["listData"]["attributes"]["names"])
    for idx, colname in enumerate(col_names):
        data[colname] = _dispatcher(robject["attributes"]["listData"]["data"][idx])

    index = None
    if robject["attributes"]["rownames"]["data"]:
        index = _dispatcher(robject["attributes"]["rownames"])

    df = BiocFrame(
        data,
        # column_names=col_names,
        row_names=index,
    )

    return df
