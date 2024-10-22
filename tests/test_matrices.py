import pytest

from rds2py import read_rds
import numpy as np
from scipy import sparse as sp

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_s4_matrix_dgc():
    array = read_rds("tests/data/s4_matrix.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_s4_matrix_dgt():
    array = read_rds("tests/data/s4_matrix_dgt.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_dense_numpy_dtype():
    array = read_rds("tests/data/numpy_dtype.rds")

    assert array is not None
    assert isinstance(array, np.ndarray)
