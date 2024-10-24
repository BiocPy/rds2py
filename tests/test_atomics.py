import pytest

from rds2py import read_rds

from biocutils import BooleanList, FloatList, IntegerList, StringList

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
