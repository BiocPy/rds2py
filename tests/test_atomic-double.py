import pytest

from rds2py import read_rds
from biocutils import FloatList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_double():
    obj = read_rds("tests/data/atomic_double.rds")

    assert obj is not None
    assert isinstance(obj, FloatList)
    assert len(obj) == 99
