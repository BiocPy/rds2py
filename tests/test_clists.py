import compressed_lists as clist

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_compressed_lists_int():
    obj = read_rds("tests/data/compressedlist_int.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, clist.CompressedIntegerList)
    assert obj.to_list() == [[11, 12], [None], [3, 2, 1, 0, -1, -2]]


def test_compressed_lists_char():
    obj = read_rds("tests/data/compressedlist_char.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, clist.CompressedCharacterList)
    assert obj.to_list() == [["A", "B", "C", "D", "E"], ["T", "U", "V", "W", "X"]]


def test_compressed_lists_floats():
    obj = read_rds("tests/data/compressedlist_numeric.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, clist.CompressedFloatList)
    assert obj.to_list() == [[11.1], [12.2], [13.3], [14.4], [15.5]]


def test_compressed_lists_bool():
    obj = read_rds("tests/data/compressedlist_logical.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, clist.CompressedBooleanList)
    assert obj.to_list() == [[True], [False], [True]]


def test_compressed_lists_dframe():
    obj = read_rds("tests/data/compressedlist_splitdframe.rds")

    assert obj is not None
    assert len(obj) > 0

    assert isinstance(obj, clist.CompressedSplitBiocFrameList)
    assert obj.unlist().shape == (153, 6)
