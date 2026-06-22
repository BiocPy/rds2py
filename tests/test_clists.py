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


def test_compressed_lists_errors():
    import pytest

    from rds2py.read_compressed_list import (
        _get_compressed_common_attrs,
        read_compressed_boolean_list,
        read_compressed_character_list,
        read_compressed_float_list,
        read_compressed_frame_list,
        read_compressed_integer_list,
        read_compressed_string_list,
        read_partitioning_by_end,
    )

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(RuntimeError):
        read_partitioning_by_end(bad_obj)

    with pytest.raises(RuntimeError):
        read_compressed_integer_list(bad_obj)

    with pytest.raises(RuntimeError):
        read_compressed_string_list(bad_obj)

    with pytest.raises(RuntimeError):
        read_compressed_boolean_list(bad_obj)

    with pytest.raises(RuntimeError):
        read_compressed_float_list(bad_obj)

    with pytest.raises(RuntimeError):
        read_compressed_frame_list(bad_obj)

    with pytest.raises(ValueError):
        _get_compressed_common_attrs({"attributes": {}})

    with pytest.raises(RuntimeError):
        read_compressed_character_list(bad_obj)

    res = _get_compressed_common_attrs(
        {"attributes": {"unlistData": {"type": "integer", "data": [1], "class_name": "integer_vector"}}}
    )
    assert res[0][0] == 1
    assert res[1] is None
    assert res[2] is None
    assert res[3] is None


def test_save_all_compressed_list_classes():
    import os
    import tempfile

    from rds2py import read_rds, save_rds, write_rds

    for file_name, expected_class in [
        ("tests/data/compressedlist_char.rds", clist.CompressedCharacterList),
        ("tests/data/compressedlist_numeric.rds", clist.CompressedFloatList),
        ("tests/data/compressedlist_logical.rds", clist.CompressedBooleanList),
        ("tests/data/compressedlist_splitdframe.rds", clist.CompressedSplitBiocFrameList),
    ]:
        obj = read_rds(file_name)
        res = save_rds(obj)
        assert isinstance(res, dict)
        assert res["type"] == "S4"

        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
            rds_path = tmp.name
        try:
            write_rds(obj, rds_path)
            recreated = read_rds(rds_path)
            assert isinstance(recreated, expected_class)
        finally:
            if os.path.exists(rds_path):
                os.unlink(rds_path)

    obj_int = read_rds("tests/data/compressedlist_int.rds")
    part = obj_int.paritioning if hasattr(obj_int, "paritioning") else obj_int.partitioning
    res_part = save_rds(part)
    assert isinstance(res_part, dict)
    assert res_part["type"] == "S4"

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        rds_path = tmp.name
    try:
        write_rds(part, rds_path)
        recreated_part = read_rds(rds_path)
        assert isinstance(recreated_part, clist.Partitioning)
    finally:
        if os.path.exists(rds_path):
            os.unlink(rds_path)


def test_clist_fallback_get():
    import os
    import tempfile

    from rds2py import read_rds, write_rds

    obj = read_rds("tests/data/compressedlist_int.rds")

    orig_get_names = clist.Partitioning.get_names
    try:
        del clist.Partitioning.get_names
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
            rds_path = tmp.name
        try:
            write_rds(obj, rds_path)
            recreated = read_rds(rds_path)
            assert isinstance(recreated, clist.CompressedIntegerList)
        finally:
            if os.path.exists(rds_path):
                os.unlink(rds_path)
    finally:
        clist.Partitioning.get_names = orig_get_names
