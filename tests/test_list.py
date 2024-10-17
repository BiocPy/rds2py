import pytest

from rds2py import read_rds

from biocutils import BooleanList, FloatList, IntegerList, StringList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_lists():
    array = read_rds("tests/data/lists.rds")

    assert array is not None
    assert len(array) > 0


# def test_read_atomic_lists_nested():
#     array = read_rds("tests/data/lists_nested.rds")

#     assert array is not None
#     assert len(array) > 0


# def test_read_atomic_lists_nested_deep():
#     array = read_rds("tests/data/lists_nested_deep.rds")

#     assert array is not None
#     assert len(array) > 0


# def test_read_atomic_lists_df():
#     array = read_rds("tests/data/lists_df.rds")

#     assert array is not None
#     assert len(array) > 0


# def test_read_atomic_lists_nested_deep_rownames():
#     array = read_rds("tests/data/lists_df_rownames.rds")

#     assert array is not None
#     assert len(array) > 0
