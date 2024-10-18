import pytest

from rds2py.PyRdsReader import PyRdsReader

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_attrs():
    parsed_obj = PyRdsReader("tests/data/atomic_attr.rds")
    print(parsed_obj)
    data = parsed_obj.read()
    print(data)

    assert data is not None
    assert len(data["data"]) > 0
    assert len(data["attributes"]) >0
    assert len(data["attributes"]["names"]["data"]) != 0
