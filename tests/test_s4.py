# import pytest

from rds2py.PyRdsReader import PyRdsParser

# __author__ = "jkanche"
# __copyright__ = "jkanche"
# __license__ = "MIT"


def test_read_s4_class():
    parsed_obj = PyRdsParser("tests/data/s4_class.rds")
    robject_obj = parsed_obj.parse()

    assert robject_obj is not None


def test_read_s4_matrix():
    parsed_obj = PyRdsParser("tests/data/s4_matrix.rds")
    robject_obj = parsed_obj.parse()

    assert robject_obj is not None


def test_read_s4_matrix_dgt():
    parsed_obj = PyRdsParser("tests/data/s4_matrix_dgt.rds")
    robject_obj = parsed_obj.parse()

    assert robject_obj is not None
