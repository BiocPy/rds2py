import pytest

from rds2py.core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

def test_read_atomic_lists():
    parsed_obj = PyParsedObject("tests/data/lists.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array) > 0

def test_read_atomic_lists_nested():
    parsed_obj = PyParsedObject("tests/data/lists_nested.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array) > 0

def test_read_atomic_lists_nested_deep():
    parsed_obj = PyParsedObject("tests/data/lists_nested_deep.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array) > 0

def test_read_atomic_lists_df():
    parsed_obj = PyParsedObject("tests/data/lists_df.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array) > 0

def test_read_atomic_lists_nested_deep():
    parsed_obj = PyParsedObject("tests/data/lists_df_rownames.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array) > 0