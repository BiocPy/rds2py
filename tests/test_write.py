import os
import tempfile

import numpy as np

from rds2py import read_rda, read_rds, write_rda, write_rds


class TestWriteRdsIntegers:
    def test_integer_array(self):
        data = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            np.testing.assert_array_equal(np.array(list(result)), data)
        finally:
            os.unlink(path)

    def test_integer_scalar(self):
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(42, path)
            result = read_rds(path)
            assert list(result) == [42]
        finally:
            os.unlink(path)

    def test_int64_array(self):
        data = np.array([10, 20, 30], dtype=np.int64)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            np.testing.assert_array_equal(np.array(list(result)), data.astype(np.int32))
        finally:
            os.unlink(path)


class TestWriteRdsDoubles:
    def test_double_array(self):
        data = np.array([1.1, 2.2, 3.3], dtype=np.float64)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            np.testing.assert_array_almost_equal(np.array(list(result)), data)
        finally:
            os.unlink(path)

    def test_float_scalar(self):
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(3.14, path)
            result = read_rds(path)
            assert abs(list(result)[0] - 3.14) < 1e-10
        finally:
            os.unlink(path)

    def test_float32_array(self):
        data = np.array([1.5, 2.5], dtype=np.float32)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            np.testing.assert_array_almost_equal(np.array(list(result)), data, decimal=5)
        finally:
            os.unlink(path)


class TestWriteRdsBooleans:
    def test_bool_array(self):
        data = np.array([True, False, True], dtype=bool)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == [True, False, True]
        finally:
            os.unlink(path)

    def test_bool_scalar(self):
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(True, path)
            result = read_rds(path)
            assert list(result) == [True]
        finally:
            os.unlink(path)


class TestWriteRdsStrings:
    def test_string_list(self):
        data = ["hello", "world", "foo"]
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == data
        finally:
            os.unlink(path)

    def test_string_scalar(self):
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds("test", path)
            result = read_rds(path)
            assert list(result) == ["test"]
        finally:
            os.unlink(path)

    def test_unicode_strings(self):
        data = ["α-globin", "fußball"]
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == data
        finally:
            os.unlink(path)


class TestWriteRdsNull:
    def test_none(self):
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(None, path)
            result = read_rds(path)
            assert result is None
        finally:
            os.unlink(path)


class TestWriteRdsDict:
    def test_named_list(self):
        data = {"a": np.array([1, 2, 3], dtype=np.int32), "b": ["x", "y"]}
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert isinstance(result, dict)
            assert set(result.keys()) == {"a", "b"}
        finally:
            os.unlink(path)

    def test_nested_dict(self):
        data = {"outer": {"inner_a": 1, "inner_b": 2.5}}
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert isinstance(result, dict)
            assert "outer" in result
        finally:
            os.unlink(path)


class TestWriteRdsList:
    def test_generic_list(self):
        data = [np.array([1, 2], dtype=np.int32), ["a", "b"], 3.14]
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            # read back as raw parsed dict to verify structure
            from rds2py.rdsutils import parse_rds

            result = parse_rds(path)
            assert result["type"] == "vector"
            assert len(result["data"]) == 3
        finally:
            os.unlink(path)


class TestWriteRdsBiocUtilsLists:
    def test_integer_list(self):
        from biocutils import IntegerList

        data = IntegerList([1, 2, 3, 4, 5])
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == [1, 2, 3, 4, 5]
        finally:
            os.unlink(path)

    def test_float_list(self):
        from biocutils import FloatList

        data = FloatList([1.1, 2.2, 3.3])
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            np.testing.assert_array_almost_equal(list(result), [1.1, 2.2, 3.3])
        finally:
            os.unlink(path)

    def test_string_list(self):
        from biocutils import StringList

        data = StringList(["hello", "world"])
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == ["hello", "world"]
        finally:
            os.unlink(path)

    def test_boolean_list(self):
        from biocutils import BooleanList

        data = BooleanList([True, False, True])
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == [True, False, True]
        finally:
            os.unlink(path)


class TestWriteRda:
    def test_write_multiple_objects(self):
        objects = {
            "int_vec": np.array([1, 2, 3], dtype=np.int32),
            "dbl_vec": np.array([1.1, 2.2, 3.3]),
            "str_vec": ["a", "b", "c"],
            "bool_vec": np.array([True, False], dtype=bool),
        }
        with tempfile.NamedTemporaryFile(suffix=".RData", delete=False) as f:
            path = f.name
        try:
            write_rda(objects, path)
            result = read_rda(path)
            assert set(result.keys()) == {"int_vec", "dbl_vec", "str_vec", "bool_vec"}
        finally:
            os.unlink(path)

    def test_write_single_object(self):
        objects = {"my_data": np.array([10, 20, 30], dtype=np.int32)}
        with tempfile.NamedTemporaryFile(suffix=".RData", delete=False) as f:
            path = f.name
        try:
            write_rda(objects, path)
            result = read_rda(path)
            assert "my_data" in result
            np.testing.assert_array_equal(np.array(list(result["my_data"])), [10, 20, 30])
        finally:
            os.unlink(path)

    def test_write_dict_object(self):
        objects = {"my_list": {"x": 1, "y": 2.5, "z": ["a", "b"]}}
        with tempfile.NamedTemporaryFile(suffix=".RData", delete=False) as f:
            path = f.name
        try:
            write_rda(objects, path)
            result = read_rda(path)
            assert "my_list" in result
            assert isinstance(result["my_list"], dict)
        finally:
            os.unlink(path)

    def test_write_none_object(self):
        objects = {"empty": None, "data": np.array([1, 2], dtype=np.int32)}
        with tempfile.NamedTemporaryFile(suffix=".RData", delete=False) as f:
            path = f.name
        try:
            write_rda(objects, path)
            result = read_rda(path)
            assert "empty" in result
            assert result["empty"] is None
            assert "data" in result
        finally:
            os.unlink(path)


class TestWriteRdsRoundtripWithR:
    """Verify written files can be read again."""

    def test_roundtrip_integers(self):
        data = np.array([10, 20, 30, 40, 50], dtype=np.int32)
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            values = [int(v) for v in result]
            assert values == [10, 20, 30, 40, 50]
        finally:
            os.unlink(path)

    def test_roundtrip_strings(self):
        data = ["hello", "world"]
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            result = read_rds(path)
            assert list(result) == ["hello", "world"]
        finally:
            os.unlink(path)

    def test_roundtrip_rda(self):
        objects = {
            "nums": np.array([1.5, 2.5, 3.5]),
            "words": ["alpha", "beta"],
        }
        with tempfile.NamedTemporaryFile(suffix=".RData", delete=False) as f:
            path = f.name
        try:
            write_rda(objects, path)
            result = read_rda(path)
            np.testing.assert_array_almost_equal(list(result["nums"]), [1.5, 2.5, 3.5])
            assert list(result["words"]) == ["alpha", "beta"]
        finally:
            os.unlink(path)


def test_py_rds_parser_invalid_file():
    import pytest

    from rds2py.PyRdsReader import PyRdsParser, PyRdsParserError

    with pytest.raises(PyRdsParserError):
        PyRdsParser("non_existent_file.rds")


def test_save_rds_not_implemented():
    import pytest

    from rds2py import save_rds

    with pytest.raises(NotImplementedError):
        save_rds(object())


def test_py_rds_parser_edge_cases_and_mocks():
    from unittest.mock import MagicMock, patch

    import pytest

    from rds2py.generics import _dispatcher
    from rds2py.PyRdsReader import PyRdsParser, PyRdsParserError, RdsReader
    from rds2py.rdsutils import get_class

    with patch("rds2py.PyRdsReader.RdsObject") as mock_rds_obj_cls:
        mock_instance = MagicMock()
        mock_instance.get_robject.return_value = "not_an_RdsReader"
        mock_rds_obj_cls.return_value = mock_instance
        with pytest.raises(PyRdsParserError, match="Expected 'RdsReader' object"):
            PyRdsParser("dummy.rds")

    parser = object.__new__(PyRdsParser)

    with pytest.raises(PyRdsParserError, match="Error parsing RDS object"):
        parser.root_object = MagicMock(spec=RdsReader)
        parser.root_object.get_rtype.side_effect = Exception("test parse error")
        parser.parse()

    mock_sym = MagicMock(spec=RdsReader)
    mock_sym.get_rtype.return_value = "symbol"
    mock_sym.get_symbol_name.return_value = "custom_symbol"
    res_sym = parser._process_object(mock_sym)
    assert res_sym["name"] == "custom_symbol"
    assert res_sym["class_name"] == "symbol"

    mock_unsup = MagicMock(spec=RdsReader)
    mock_unsup.get_rtype.return_value = "unsupported_type"
    with pytest.warns(RuntimeWarning, match="Unsupported R object type: unsupported_type"):
        res_unsup = parser._process_object(mock_unsup)
        assert res_unsup["data"] is None

    with pytest.raises(PyRdsParserError, match="Error processing object"):
        mock_err = MagicMock(spec=RdsReader)
        mock_err.get_rtype.side_effect = Exception("process error")
        parser._process_object(mock_err)

    with pytest.raises(PyRdsParserError, match="Error handling R special cases"):
        parser._handle_r_special_cases(None, "integer", 0)

    with pytest.raises(PyRdsParserError, match="Error getting numeric data"):
        mock_num_err = MagicMock(spec=RdsReader)
        mock_num_err.get_numeric_data.side_effect = Exception("numeric error")
        parser._get_numeric_data(mock_num_err, "integer")

    with pytest.raises(PyRdsParserError, match="Error processing attributes"):
        mock_attr_err = MagicMock(spec=RdsReader)
        mock_attr_err.get_attribute_names.side_effect = Exception("attributes error")
        parser._process_attributes(mock_attr_err)

    mock_root = MagicMock(spec=RdsReader)
    mock_root.get_dimensions.return_value = (10, 20)
    parser.root_object = mock_root
    assert parser.get_dimensions() == (10, 20)

    mock_root.get_dimensions.side_effect = Exception("dimensions error")
    with pytest.raises(PyRdsParserError, match="Error getting dimensions"):
        parser.get_dimensions()

    with pytest.warns(RuntimeWarning, match="Failed to coerce RDS object to class"):
        res_coerce = _dispatcher({"type": "S4", "class_name": "dgCMatrix", "attributes": {}})
        assert isinstance(res_coerce, dict)

    assert get_class({"type": "integer_vector", "class_name": "integer"}) == "integer"
    assert get_class({"type": "integer_vector", "class_name": "integer", "attributes": None}) == "integer"
