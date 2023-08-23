import pytest

from rds2py.interface import as_dense_matrix, as_sparse_matrix
from rds2py.parser import read_rds
import numpy as np
from scipy import sparse as sp

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_s4_matrix_dgc():
    parsed_obj = read_rds("tests/data/s4_matrix.rds")
    array = as_sparse_matrix(parsed_obj)

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_s4_matrix_dgt():
    parsed_obj = read_rds("tests/data/s4_matrix_dgt.rds")
    array = as_sparse_matrix(parsed_obj)

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_dense_numpy_dtype():
    parsed_obj = read_rds("tests/data/numpy_dtype.rds")
    array = as_dense_matrix(parsed_obj)

    assert array is not None
    assert isinstance(array, np.ndarray)
