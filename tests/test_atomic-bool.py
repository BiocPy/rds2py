import pytest

from rds2py import read_rds
from biocutils import BooleanList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_logical():
    arr = read_rds("tests/data/atomic_logical.rds")

    assert arr is not None
    assert isinstance(arr, BooleanList)
    assert len(arr) > 0


def test_read_atomic_logical_na():
    arr = read_rds("tests/data/atomic_logical_wNA.rds")

    assert arr is not None
    assert isinstance(arr, BooleanList)
    assert len(arr) > 0
