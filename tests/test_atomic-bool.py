import pytest

from rds2py.PyRdsReader import PyRdsReader

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_logical():
    parsed_obj = PyRdsReader("tests/data/atomic_logical.rds")
    array = parsed_obj.read()

    assert array is not None
    assert array["data"].shape[0] > 0


def test_read_atomic_logical_na():
    parsed_obj = PyRdsReader("tests/data/atomic_logical_wNA.rds")
    array = parsed_obj.read()

    assert array is not None
    assert array["data"].shape[0] > 0
