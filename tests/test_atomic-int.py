import pytest

from rds2py import read_rds
from biocutils import IntegerList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_ints():
    arr = read_rds("tests/data/atomic_ints.rds")

    assert arr is not None
    assert isinstance(arr, IntegerList)
    assert len(arr) == 112


def test_read_atomic_ints_with_names():
    arr = read_rds("tests/data/atomic_ints_with_names.rds")

    assert arr is not None
    assert isinstance(arr, IntegerList)
    assert arr.names is not None
    assert len(arr) == 112
