import pytest

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_simple_lists():
    obj = read_rds("tests/data/simple_list.rds")

    assert obj is not None
    assert len(obj) > 0

    assert "collab" in obj
    assert len(obj["collab"]) > 0


def test_read_atomic_lists():
    obj = read_rds("tests/data/lists.rds")

    assert obj is not None
    assert len(obj) > 0


def test_read_atomic_lists_nested():
    obj = read_rds("tests/data/lists_nested.rds")

    assert obj is not None
    assert len(obj) > 0


def test_read_atomic_lists_nested_deep():
    obj = read_rds("tests/data/lists_nested_deep.rds")

    assert obj is not None
    assert len(obj) > 0


def test_read_atomic_lists_df():
    obj = read_rds("tests/data/lists_df.rds")

    assert obj is not None
    assert len(obj) > 0


def test_read_atomic_lists_nested_deep_rownames():
    obj = read_rds("tests/data/lists_df_rownames.rds")

    assert obj is not None
    assert len(obj) > 0
