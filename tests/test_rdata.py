"""Tests for RData (.RData/.rda) file reading."""

from rds2py.PyRdaReader import PyRdaParser

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class TestPyRdaParser:
    def test_object_names(self):
        parser = PyRdaParser("tests/data/simple.RData")
        names = parser.get_object_names()
        assert set(names) == {"int_vec", "dbl_vec", "str_vec", "bool_vec"}
