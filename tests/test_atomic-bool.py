import pytest

from rds2py.core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_logical():
    parsed_obj = PyParsedObject("tests/data/atomic_logical.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert array["data"].shape[0] > 0


def test_read_atomic_logical_na():
    parsed_obj = PyParsedObject("tests/data/atomic_logical_wNA.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert array["data"].shape[0] > 0
