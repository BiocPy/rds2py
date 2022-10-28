import pytest

from rds2py.core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_s4_class():
    parsed_obj = PyParsedObject("tests/data/s4_class.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None

def test_read_s4_matrix():
    parsed_obj = PyParsedObject("tests/data/s4_matrix.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None