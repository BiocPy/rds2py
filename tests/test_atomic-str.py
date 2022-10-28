import pytest

from rds2py.core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_chars():
    parsed_obj = PyParsedObject("tests/data/atomic_chars.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array["data"]) == 26

def test_read_atomic_chars_unicode():
    parsed_obj = PyParsedObject("tests/data/atomic_chars_unicode.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()

    assert array is not None
    assert len(array["data"]) == 4
