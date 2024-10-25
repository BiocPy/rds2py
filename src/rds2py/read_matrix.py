"""Functions and classes for parsing R matrix objects.

This module provides functionality to convert R matrix objects (both dense and sparse) into their Python equivalents
using NumPy and SciPy sparse matrix formats. It handles various R matrix types including dgCMatrix, dgRMatrix, and
dgTMatrix.
"""

from typing import Literal

from numpy import ndarray
from scipy.sparse import csc_matrix, csr_matrix, spmatrix

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class MatrixWrapper:
    """A simple wrapper class for matrices that preserves dimension names.

    This class bundles a matrix (dense or sparse) with its dimension names,
    maintaining the R-style naming of rows and columns.

    Attributes:
        matrix:
            The underlying matrix object (numpy.ndarray or scipy.sparse matrix).

        dimnames:
            A tuple of (row_names, column_names), each being a list of strings or None.
    """

    def __init__(self, matrix, dimnames=None) -> None:
        self.matrix = matrix
        self.dimnames = dimnames


def _as_sparse_matrix(robject: dict, **kwargs) -> spmatrix:
    """Convert an R sparse matrix to a SciPy sparse matrix.

    Notes:
        - Supports dgCMatrix (column-sparse)
        - Supports dgRMatrix (row-sparse)
        - Supports dgTMatrix (triplet format)
        - Preserves dimension names if present

    Args:
        robject:
            Dictionary containing parsed R sparse matrix data.

        **kwargs:
            Additional arguments.

    Returns:
        A SciPy sparse matrix or wrapped matrix if dimension names exist.
    """

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
        names = _dispatcher(robject["attributes"]["dimnames"], **kwargs)
        if names is not None and len(names) > 0:
            return MatrixWrapper(mat, names)

    return mat


def _as_dense_matrix(robject, order: Literal["C", "F"] = "F", **kwargs) -> ndarray:
    """Convert an R matrix to a `NumPy` array.

    Args:
        robject:
            Dictionary containing parsed R matrix data.

        order:
            Memory layout for the array.
            'C' for row-major, 'F' for column-major (default).

        **kwargs:
            Additional arguments.

    Returns:
        A NumPy array or wrapped array if dimension names exist.
    """
    _cls = get_class(robject)

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
        names = _dispatcher(robject["attributes"]["dimnames"], **kwargs)
        if names is not None and len(names) > 0:
            return MatrixWrapper(mat, names)

    return mat


def read_dgcmatrix(robject: dict, **kwargs) -> spmatrix:
    """Parse an R dgCMatrix (sparse column matrix).

    Args:
        robject:
            Dictionary containing parsed dgCMatrix data.

        **kwargs:
            Additional arguments.

    Returns:
        Parsed sparse column matrix.
    """
    return _as_sparse_matrix(robject, **kwargs)


def read_dgrmatrix(robject: dict, **kwargs) -> spmatrix:
    """Parse an R dgRMatrix (sparse row matrix).

    Args:
        robject:
            Dictionary containing parsed dgRMatrix data.

        **kwargs:
            Additional arguments.

    Returns:
        Parsed sparse row matrix.
    """
    return _as_sparse_matrix(robject, **kwargs)


def read_dgtmatrix(robject: dict, **kwargs) -> spmatrix:
    """Parse an R dgTMatrix (sparse triplet matrix)..

    Args:
        robject:
            Dictionary containing parsed dgTMatrix data.

        **kwargs:
            Additional arguments.

    Returns:
        Parsed sparse matrix.
    """
    return _as_sparse_matrix(robject, **kwargs)


def read_ndarray(robject: dict, order: Literal["C", "F"] = "F", **kwargs) -> ndarray:
    """Parse an R matrix as a NumPy array.

    Args:
        robject:
            Dictionary containing parsed dgCMatrix data.

        order:
            Memory layout for the array.

        **kwargs:
            Additional arguments.

    Returns:
        Parsed dense array.
    """
    return _as_dense_matrix(robject, order=order, **kwargs)
