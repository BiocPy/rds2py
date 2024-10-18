import pytest

from rds2py.PyRdsReader import PyRdsReader

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_chars():
    parsed_obj = PyRdsReader("tests/data/atomic_chars.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array["data"]) == 26


def test_read_atomic_chars_unicode():
    parsed_obj = PyRdsReader("tests/data/atomic_chars_unicode.rds")
    array = parsed_obj.read()

    assert array is not None
    assert len(array["data"]) == 4
