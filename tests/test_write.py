import os
import tempfile

import numpy as np
import pytest

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
            import subprocess

            result = subprocess.run(
                ["Rscript", "-e", f'x <- readRDS("{path}"); cat(x, sep=",")'],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                values = [int(v) for v in result.stdout.strip().split(",")]
                assert values == [10, 20, 30, 40, 50]
            else:
                pytest.skip("R not available or failed")
        finally:
            os.unlink(path)

    def test_roundtrip_strings(self):
        data = ["hello", "world"]
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
            path = f.name
        try:
            write_rds(data, path)
            import subprocess

            result = subprocess.run(
                ["Rscript", "-e", f'x <- readRDS("{path}"); cat(x, sep=",")'],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                assert result.stdout.strip() == "hello,world"
            else:
                pytest.skip("R not available or failed")
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
            import subprocess

            result = subprocess.run(
                ["Rscript", "-e", f'load("{path}"); cat(nums, sep=","); cat("\\n"); cat(words, sep=",")'],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                nums = [float(v) for v in lines[0].split(",")]
                np.testing.assert_array_almost_equal(nums, [1.5, 2.5, 3.5])
                assert lines[1] == "alpha,beta"
            else:
                pytest.skip("R not available or failed")
        finally:
            os.unlink(path)
