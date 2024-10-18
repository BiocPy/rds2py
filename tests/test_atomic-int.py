import pytest

from rds2py.lib_rds import PyRdsObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_ints():
    parsed_obj = PyRdsObject("tests/data/atomic_ints.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    print(array)
    assert array["data"].shape[0] == 112
