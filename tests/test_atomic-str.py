import pytest

from rds2py import read_rds
from biocutils import StringList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_chars():
    arr = read_rds("tests/data/atomic_chars.rds")

    assert arr is not None
    assert isinstance(arr, StringList)
    assert len(arr) == 26


def test_read_atomic_chars_unicode():
    arr = read_rds("tests/data/atomic_chars_unicode.rds")

    assert arr is not None
    assert isinstance(arr, StringList)
    assert len(arr) == 4
