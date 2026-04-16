import numpy as np
import pytest

from rds2py import parse_rda, read_rda
from rds2py.PyRdaReader import PyRdaParser, PyRdaParserError

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class TestPyRdaParser:
    def test_object_names(self):
        parser = PyRdaParser("tests/data/simple.RData")
        names = parser.get_object_names()
        assert set(names) == {"int_vec", "dbl_vec", "str_vec", "bool_vec"}

    def test_object_count(self):
        parser = PyRdaParser("tests/data/simple.RData")
        assert parser.get_object_count() == 4

    def test_parse_all(self):
        parser = PyRdaParser("tests/data/simple.RData")
        result = parser.parse()
        assert isinstance(result, dict)
        assert set(result.keys()) == {"int_vec", "dbl_vec", "str_vec", "bool_vec"}

    def test_parse_single_object(self):
        parser = PyRdaParser("tests/data/simple.RData")
        obj = parser.parse_object("int_vec")
        assert obj["type"] == "integer"

    def test_parse_missing_object(self):
        parser = PyRdaParser("tests/data/simple.RData")
        with pytest.raises(PyRdaParserError):
            parser.parse_object("nonexistent")

    def test_invalid_file(self):
        with pytest.raises(PyRdaParserError):
            PyRdaParser("tests/data/nonexistent.RData")

    def test_single_object_file(self):
        parser = PyRdaParser("tests/data/single_object.RData")
        names = parser.get_object_names()
        assert names == ["single_obj"]
        assert parser.get_object_count() == 1


class TestParseRda:
    def test_parse_all_objects(self):
        result = parse_rda("tests/data/simple.RData")
        assert isinstance(result, dict)
        assert "int_vec" in result
        assert "dbl_vec" in result
        assert "str_vec" in result
        assert "bool_vec" in result

    def test_parse_selected_objects(self):
        result = parse_rda("tests/data/simple.RData", objects=["int_vec", "dbl_vec"])
        assert set(result.keys()) == {"int_vec", "dbl_vec"}

    def test_integer_data(self):
        result = parse_rda("tests/data/simple.RData", objects=["int_vec"])
        obj = result["int_vec"]
        assert obj["type"] == "integer"
        data = obj["data"]
        np.testing.assert_array_equal(data, [1, 2, 3, 4, 5])

    def test_double_data(self):
        result = parse_rda("tests/data/simple.RData", objects=["dbl_vec"])
        obj = result["dbl_vec"]
        assert obj["type"] == "double"
        data = obj["data"]
        np.testing.assert_array_almost_equal(data, [1.1, 2.2, 3.3, 4.4, 5.5])

    def test_string_data(self):
        result = parse_rda("tests/data/simple.RData", objects=["str_vec"])
        obj = result["str_vec"]
        assert obj["type"] == "string"
        assert list(obj["data"]) == ["hello", "world", "foo"]

    def test_boolean_data(self):
        result = parse_rda("tests/data/simple.RData", objects=["bool_vec"])
        obj = result["bool_vec"]
        assert obj["type"] == "boolean"

    def test_single_object_file(self):
        result = parse_rda("tests/data/single_object.RData")
        assert "single_obj" in result
        obj = result["single_obj"]
        assert obj["type"] == "integer"

    def test_mixed_types(self):
        result = parse_rda("tests/data/mixed.RData")
        assert "nums" in result
        assert "chars" in result
        assert "ints" in result
        assert "nested_list" in result

        assert result["nums"]["type"] == "double"
        assert result["chars"]["type"] == "string"
        assert result["ints"]["type"] == "integer"
        assert result["nested_list"]["type"] == "vector"


class TestReadRda:
    def test_read_all(self):
        result = read_rda("tests/data/simple.RData")
        assert isinstance(result, dict)
        assert len(result) == 4

    def test_read_selected(self):
        result = read_rda("tests/data/simple.RData", objects=["int_vec"])
        assert set(result.keys()) == {"int_vec"}

    def test_read_list(self):
        result = read_rda("tests/data/list.RData")
        assert "test_list" in result

    def test_read_mixed(self):
        result = read_rda("tests/data/mixed.RData")
        assert "nums" in result
        assert "chars" in result
        assert "ints" in result
        assert "nested_list" in result

    def test_read_single_object(self):
        result = read_rda("tests/data/single_object.RData")
        assert "single_obj" in result
