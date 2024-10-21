import pytest

from rds2py.PyRdsReader import PyRdsParser

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_attrs():
    parsed_obj = PyRdsParser("tests/data/atomic_attr.rds")
    data = parsed_obj.parse()
    print(data)

    assert data is not None
    assert len(data["data"]) > 0
    assert len(data["attributes"]) > 0
    assert len(data["attributes"]["names"]["data"]) == 1000
