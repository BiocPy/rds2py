import pytest

from rds2py import read_rds
from compressed_lists import CompressedIntegerList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_compressed_lists_int():
    obj = read_rds("tests/data/compressedlist_int.rds")

    print(obj)

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, CompressedIntegerList)

