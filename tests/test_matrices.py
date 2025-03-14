import pytest

from rds2py import read_rds
import numpy as np
from scipy import sparse as sp

from rds2py.read_matrix import MatrixWrapper

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_s4_matrix_dgc():
    array = read_rds("tests/data/s4_matrix.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)

def test_read_s4_matrix_dgc_with_rownames():
    array = read_rds("tests/data/matrix_with_row_names.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert len(array.dimnames[0]) == 100
    assert array.dimnames[1] is None


def test_read_s4_matrix_dgc_with_bothnames():
    array = read_rds("tests/data/matrix_with_dim_names.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert len(array.dimnames[0]) == 100
    assert len(array.dimnames[1]) == 10

def test_read_s4_matrix_dgt():
    array = read_rds("tests/data/s4_matrix_dgt.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_dense_numpy_dtype():
    array = read_rds("tests/data/numpy_dtype.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert isinstance(array.matrix, np.ndarray)
    assert array.dimnames is not None
    assert len(array.dimnames) == len(array.matrix.shape)
