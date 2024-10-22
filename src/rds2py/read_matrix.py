from typing import Literal


from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _as_sparse_matrix(robj: dict):
    """Parse an R object as a sparse matrix.

    Only supports reading of `dgCMatrix`, `dgRMatrix`, `dgTMatrix` marices.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A sparse matrix of the R object.
    """
    from scipy.sparse import csc_matrix, csr_matrix

    _cls = get_class(robj)

    if _cls not in ["dgCMatrix", "dgRMatrix", "dgTMatrix"]:
        raise TypeError(
            f"`robj` does not contain not a supported sparse matrix format, contains `{_cls}`."
        )

    if _cls == "dgCMatrix":
        return csc_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgRMatrix":
        return csr_matrix(
            (
                robj["attributes"]["x"]["data"],
                robj["attributes"]["i"]["data"],
                robj["attributes"]["p"]["data"],
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgTMatrix":
        return csr_matrix(
            (
                robj["attributes"]["x"]["data"],
                (
                    robj["attributes"]["i"]["data"],
                    robj["attributes"]["j"]["data"],
                ),
            ),
            shape=tuple(robj["attributes"]["Dim"]["data"].tolist()),
        )


def _as_dense_matrix(robj, order: Literal["C", "F"] = "F"):
    """Parse an R object as a :py:class:`~numpy.ndarray`.

    Args:
        robj:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

        order:
            Row-major (**C**-style) or Column-major (**F**ortran-style)
            order.

            Defaults to "F".

    Returns:
        An ``ndarray`` of the R object.
    """
    _cls = get_class(robj)

    from numpy import ndarray

    if order not in ["C", "F"]:
        raise ValueError("order must be either 'C' or 'F'.")

    if _cls not in ["ndarray"]:
        raise TypeError(f"obj is not a supported dense matrix format, but is `{_cls}`.")

    return ndarray(
        shape=tuple(robj["attributes"]["dim"]["data"].tolist()),
        dtype=robj["data"].dtype,
        buffer=robj["data"],
        order=order,
    )


def parse_dgcmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_dgrmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_dgtmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_ndarray(robject: dict, order: Literal["C", "F"] = "F"):
    return _as_dense_matrix(robject, order=order)
