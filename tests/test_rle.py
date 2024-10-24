import pytest

from rds2py import read_rds

from biocutils import BooleanList, FloatList, IntegerList, StringList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

## With attributes


def test_read_simple_rle():
    data = read_rds("tests/data/simple_rle.rds")

    assert data is not None
    assert len(data) == 36
