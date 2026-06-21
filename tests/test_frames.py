from biocframe import BiocFrame

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_lists_df():
    frame = read_rds("tests/data/lists_df.rds")

    assert frame is not None
    assert isinstance(frame, BiocFrame)
    assert len(frame) > 0


def test_read_atomic_lists_nested_deep_rownames():
    frame = read_rds("tests/data/lists_df_rownames.rds")

    assert frame is not None
    assert isinstance(frame, BiocFrame)
    assert len(frame) > 0


def test_read_frame_errors():
    import pytest

    from rds2py.read_frame import read_data_frame, read_dframe

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(RuntimeError):
        read_data_frame({"type": "vector", "attributes": {"class": {"data": ["bad"]}}})

    with pytest.raises(RuntimeError):
        read_dframe(bad_obj)
