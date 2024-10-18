import pytest

from rds2py.PyRdsReader import PyRdsReader

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_lists():
    parsed_obj = PyRdsReader("tests/data/lists.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array) > 0


def test_read_atomic_lists_nested():
    parsed_obj = PyRdsReader("tests/data/lists_nested.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array) > 0


def test_read_atomic_lists_nested_deep():
    parsed_obj = PyRdsReader("tests/data/lists_nested_deep.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array) > 0


def test_read_atomic_lists_df():
    parsed_obj = PyRdsReader("tests/data/lists_df.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array) > 0


def test_read_atomic_lists_nested_deep_rownames():
    parsed_obj = PyRdsReader("tests/data/lists_df_rownames.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array) > 0
