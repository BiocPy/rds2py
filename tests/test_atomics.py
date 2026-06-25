from biocutils import BooleanList, FloatList, IntegerList, StringList

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

## With attributes


def test_read_atomic_attrs():
    data = read_rds("tests/data/atomic_attr.rds")

    assert data is not None
    assert isinstance(data, dict)
    assert data["attributes"]["class"]["data"][0] == "frog"


## Booleans


def test_read_atomic_logical():
    arr = read_rds("tests/data/atomic_logical.rds")

    assert arr is not None
    assert isinstance(arr, BooleanList)
    assert len(arr) > 0


def test_read_atomic_logical_na():
    arr = read_rds("tests/data/atomic_logical_wNA.rds")

    assert arr is not None
    assert isinstance(arr, BooleanList)
    assert len(arr) > 0


## Doubles/Floats


def test_read_atomic_double():
    obj = read_rds("tests/data/atomic_double.rds")

    assert obj is not None
    assert isinstance(obj, FloatList)
    assert len(obj) == 99


## Ints


def test_read_atomic_ints():
    arr = read_rds("tests/data/atomic_ints.rds")

    assert arr is not None
    assert isinstance(arr, IntegerList)
    assert len(arr) == 112
    assert arr.names is None


def test_read_atomic_ints_with_names():
    arr = read_rds("tests/data/atomic_ints_with_names.rds")

    assert arr is not None
    assert isinstance(arr, IntegerList)
    assert arr.names is not None
    assert len(arr) == 112


## Strings


def test_read_atomic_chars():
    arr = read_rds("tests/data/atomic_chars.rds")

    assert arr is not None
    assert isinstance(arr, StringList)
    assert len(arr) == 26
    assert arr.names is None


def test_read_atomic_chars_unicode():
    arr = read_rds("tests/data/atomic_chars_unicode.rds")

    assert arr is not None
    assert isinstance(arr, StringList)
    assert len(arr) == 4
    assert arr.names is None


## Test scalar values, defaults to a vector


def test_read_scalar_float():
    obj = read_rds("tests/data/scalar_int.rds")

    assert obj is not None
    assert isinstance(obj, FloatList)
    assert len(obj) == 1
    assert obj[0] == 10.0


def test_save_names_directly():
    import os
    import tempfile

    from biocutils import Names

    from rds2py import write_rds

    names_obj = Names(["a", "b", "c"])
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name

    try:
        write_rds(names_obj, path)
        assert os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_save_numpy_scalars():
    import numpy as np
    from rds2py import save_rds

    # Test integer scalar
    i_scalar = np.int32(42)
    res_i = save_rds(i_scalar)
    assert isinstance(res_i, int)
    assert res_i == 42

    # Test float scalar
    f_scalar = np.float64(3.14)
    res_f = save_rds(f_scalar)
    assert isinstance(res_f, float)
    assert res_f == 3.14

    # Test bool scalar
    b_scalar = np.bool_(True)
    res_b = save_rds(b_scalar)
    assert isinstance(res_b, bool)
    assert res_b is True

    # Test string scalar
    s_scalar = np.str_("hello")
    res_s = save_rds(s_scalar)
    assert isinstance(res_s, str)
    assert res_s == "hello"

