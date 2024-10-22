from typing import Literal

from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _as_sparse_matrix(robject: dict):
    """Parse an R object as a sparse matrix.

    Only supports reading of `dgCMatrix`, `dgRMatrix`, `dgTMatrix` marices.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        A sparse matrix of the R object.
    """
    from scipy.sparse import csc_matrix, csr_matrix

    _cls = get_class(robject)

    if _cls not in ["dgCMatrix", "dgRMatrix", "dgTMatrix"]:
        raise RuntimeError(
            f"`robject` does not contain not a supported sparse matrix format, contains `{_cls}`."
        )

    if _cls == "dgCMatrix":
        return csc_matrix(
            (
                robject["attributes"]["x"]["data"],
                robject["attributes"]["i"]["data"],
                robject["attributes"]["p"]["data"],
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgRMatrix":
        return csr_matrix(
            (
                robject["attributes"]["x"]["data"],
                robject["attributes"]["i"]["data"],
                robject["attributes"]["p"]["data"],
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )

    if _cls == "dgTMatrix":
        return csr_matrix(
            (
                robject["attributes"]["x"]["data"],
                (
                    robject["attributes"]["i"]["data"],
                    robject["attributes"]["j"]["data"],
                ),
            ),
            shape=tuple(robject["attributes"]["Dim"]["data"].tolist()),
        )


def _as_dense_matrix(robject, order: Literal["C", "F"] = "F"):
    """Parse an R object as a :py:class:`~numpy.ndarray`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

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

    return ndarray(
        shape=tuple(robject["attributes"]["dim"]["data"].tolist()),
        dtype=robject["data"].dtype,
        buffer=robject["data"],
        order=order,
    )


def parse_dgcmatrix(robjectect: dict):
    return _as_sparse_matrix(robjectect)


def parse_dgrmatrix(robjectect: dict):
    return _as_sparse_matrix(robjectect)


def parse_dgtmatrix(robjectect: dict):
    return _as_sparse_matrix(robjectect)


def parse_ndarray(robjectect: dict, order: Literal["C", "F"] = "F"):
    return _as_dense_matrix(robjectect, order=order)
