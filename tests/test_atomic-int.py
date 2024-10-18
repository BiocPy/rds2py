import pytest

from rds2py.PyRdsReader import PyRdsReader

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_ints():
    parsed_obj = PyRdsReader("tests/data/atomic_ints.rds")
    array = parsed_obj.read()

    assert array is not None
    print(array)
    assert array["data"].shape[0] == 112
