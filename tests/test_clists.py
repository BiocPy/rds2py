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


def test_save_compressed_lists():
    import os
    import tempfile

    from rds2py import save_rds, write_rds

    obj = read_rds("tests/data/compressedlist_int.rds")

    res = save_rds(obj)
    assert isinstance(res, dict)
    assert res["type"] == "S4"
    assert res["class_name"] == "CompressedIntegerList"
    assert "unlistData" in res["attributes"]
    assert "partitioning" in res["attributes"]

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        rds_path = tmp.name
    try:
        write_rds(obj, rds_path)
        from rds2py.rdsutils import parse_rds

        parsed = parse_rds(rds_path)
        assert parsed["type"] == "S4"
        assert parsed["class_name"] == "CompressedIntegerList"

        recreated = read_rds(rds_path)
        assert isinstance(recreated, type(obj))
        assert recreated.to_list() == obj.to_list()
    finally:
        if os.path.exists(rds_path):
            os.unlink(rds_path)
