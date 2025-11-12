from compressed_lists import CompressedIntegerList

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_compressed_lists_int():
    obj = read_rds("tests/data/compressedlist_int.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, CompressedIntegerList)
    assert obj.to_list().as_list() == [11, 12, 3, 2, 1, 0, -1, -2]
