from typing import Any, Literal

from numpy import ndarray
from scipy.sparse import spmatrix

from .rdsutils import get_class
from .generics import _dispatcher

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class MatrixWrapper:
    def __init__(self, matrix, dimnames=None) -> None:
        self.matrix = matrix
        self.dimnames = dimnames


def _as_sparse_matrix(robject: dict):
    """Parse an R object as a sparse matrix.

    Only supports reading of `dgCMatrix`, `dgRMatrix`, `dgTMatrix` marices.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A sparse matrix of the R object.
    """
    from scipy.sparse import csc_matrix, csr_matrix

    _cls = get_class(robject)

    if _cls not in ["dgCMatrix", "dgRMatrix", "dgTMatrix"]:
        raise RuntimeError(f"`robject` does not contain not a supported sparse matrix format, contains `{_cls}`.")

    if _cls == "dgCMatrix":
        mat = csc_matrix(
            (
                robject["attributes"]["x"]["data"],
                robject["attributes"]["i"]["data"],
                robject["attributes"]["p"]["data"],
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )
    elif _cls == "dgRMatrix":
        mat = csr_matrix(
            (
                robject["attributes"]["x"]["data"],
                robject["attributes"]["i"]["data"],
                robject["attributes"]["p"]["data"],
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )
    elif _cls == "dgTMatrix":
        mat = csr_matrix(
            (
                robject["attributes"]["x"]["data"],
                (
                    robject["attributes"]["i"]["data"],
                    robject["attributes"]["j"]["data"],
                ),
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )

    names = None
    if "dimnames" in robject["attributes"]:
        names = _dispatcher(robject["attributes"]["dimnames"])
        if names is not None and len(names) > 0:
            return MatrixWrapper(mat, names)

    return mat


def _as_dense_matrix(robject, order: Literal["C", "F"] = "F"):
    """Parse an R object as a :py:class:`~numpy.ndarray`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

        order:
            Row-major (**C**-style) or Column-major (**F**ortran-style)
            order.

            Defaults to "F".

    Returns:
        An ``ndarray`` of the R object.
    """
    _cls = get_class(robject)

    from numpy import ndarray

    if order not in ["C", "F"]:
        raise ValueError("order must be either 'C' or 'F'.")

    if _cls not in ["ndarray"]:
        raise TypeError(f"obj is not a supported dense matrix format, but is `{_cls}`.")

    mat = ndarray(
        shape=tuple(robject["attributes"]["dim"]["data"].tolist()),
        dtype=robject["data"].dtype,
        buffer=robject["data"],
        order=order,
    )

    names = None
    if "dimnames" in robject["attributes"]:
        names = _dispatcher(robject["attributes"]["dimnames"])
        if names is not None and len(names) > 0:
            return MatrixWrapper(mat, names)

    return mat


def parse_dgcmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_dgrmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_dgtmatrix(robject: dict):
    return _as_sparse_matrix(robject)


def parse_ndarray(robject: dict, order: Literal["C", "F"] = "F"):
    return _as_dense_matrix(robject, order=order)
