from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_data_frame(robj):
    """Read an R object to a :py:class:`~biocframe.BiocFrame`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from biocframe import BiocFrame

    cls = get_class(robj)

    if cls != "data.frame":
        raise TypeError("`robj` does not contain a 'data.frame'.")

    col_names = _dispatcher(robj["attributes"]["names"])

    bframe_obj = {}
    for idx, rd in enumerate(robj["data"]):
        bframe_obj[col_names[idx]] = _dispatcher(rd)

    df = BiocFrame(
        bframe_obj,
        row_names=_dispatcher(robj["attributes"]["row.names"]),
    )

    return df


def parse_dframe(robj):
    """Convert a realized R object to a pandas data frame representation.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A `DataFrame` from the R Object.
    """
    from biocframe import BiocFrame

    cls = get_class(robj)

    if cls != "DFrame":
        raise Exception("`robj` does not contain a 'DFrame'.")

    data = {}
    col_names = _dispatcher(robj["attributes"]["listData"]["attributes"]["names"])
    for idx in range(len(col_names)):
        idx_asy = _dispatcher(robj["attributes"]["listData"]["data"][idx])

        data[col_names[idx]] = idx_asy["data"]

    index = None
    if robj["attributes"]["rownames"]["data"]:
        index = _dispatcher(robj["attributes"]["rownames"])

    df = BiocFrame(
        data,
        # column_names=col_names,
        row_names=index,
    )

    return df
