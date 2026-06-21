import numpy as np
from scipy import sparse as sp

from rds2py import read_rds
from rds2py.read_matrix import MatrixWrapper

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_s4_matrix_dgc():
    array = read_rds("tests/data/s4_matrix.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_s4_matrix_dgc_with_rownames():
    array = read_rds("tests/data/matrix_with_row_names.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert len(array.dimnames[0]) == 100
    assert array.dimnames[1] is None


def test_read_s4_matrix_dgc_with_bothnames():
    array = read_rds("tests/data/matrix_with_dim_names.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert len(array.dimnames[0]) == 100
    assert len(array.dimnames[1]) == 10


def test_read_s4_matrix_dgt():
    array = read_rds("tests/data/s4_matrix_dgt.rds")

    assert array is not None
    assert isinstance(array, sp.spmatrix)


def test_read_dense_numpy_dtype():
    array = read_rds("tests/data/numpy_dtype.rds")

    assert array is not None
    assert isinstance(array, MatrixWrapper)
    assert isinstance(array.matrix, np.ndarray)
    assert array.dimnames is not None
    assert len(array.dimnames) == len(array.matrix.shape)


def test_save_matrix_integer():
    from rds2py import save_rds

    mat = np.array([[1, 2], [3, 4]], dtype=np.int32)
    res = save_rds(mat)
    assert res["type"] == "integer"
    assert res["attributes"]["dim"]["data"] == [2, 2]


def test_save_matrix_bool():
    from rds2py import save_rds

    mat = np.array([[True, False], [False, True]], dtype=bool)
    res = save_rds(mat)
    assert res["type"] == "logical"
    assert res["attributes"]["dim"]["data"] == [2, 2]


def test_save_matrix_wrapper_with_dimnames():
    import os
    import tempfile

    from rds2py import save_rds, write_rds

    mat = np.array([[1.0, 2.0], [3.0, 4.0]])
    wrapper = MatrixWrapper(mat, dimnames=[["r1", "r2"], ["c1", "c2"]])
    res = save_rds(wrapper)
    assert "dimnames" in res["attributes"]
    assert res["attributes"]["dimnames"]["data"][0] == ["r1", "r2"]
    assert res["attributes"]["dimnames"]["data"][1] == ["c1", "c2"]

    wrapper_partial = MatrixWrapper(mat, dimnames=[None, ["c1", "c2"]])
    res_partial = save_rds(wrapper_partial)
    assert res_partial["attributes"]["dimnames"]["data"][0]["type"] == "null"
    assert res_partial["attributes"]["dimnames"]["data"][1] == ["c1", "c2"]

    assert wrapper.shape == (2, 2)

    mat_1d = np.array([1.0, 2.0])
    wrapper_1d = MatrixWrapper(mat_1d)
    res_1d = save_rds(wrapper_1d)
    assert isinstance(res_1d, np.ndarray)

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name
    try:
        write_rds(wrapper, path)
        recreated = read_rds(path)
        assert isinstance(recreated, MatrixWrapper)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_matrix_read_errors_and_dgrmatrix():
    import pytest

    from rds2py.read_matrix import _as_dense_matrix, _as_sparse_matrix, read_dgrmatrix

    with pytest.raises(RuntimeError):
        _as_sparse_matrix({"type": "S4", "class_name": "BadClass"})

    dgr_mock = {
        "type": "S4",
        "class_name": "dgRMatrix",
        "attributes": {
            "x": {"type": "double", "data": np.array([1.0, 2.0])},
            "i": {"type": "integer", "data": np.array([0, 1])},
            "p": {"type": "integer", "data": np.array([0, 1, 2])},
            "Dim": {"type": "integer", "data": np.array([2, 2])},
        },
    }
    res_dgr = read_dgrmatrix(dgr_mock)
    assert res_dgr is not None
    assert res_dgr.shape == (2, 2)

    with pytest.raises(ValueError):
        _as_dense_matrix({"type": "ndarray"}, order="X")

    with pytest.raises(TypeError):
        _as_dense_matrix({"type": "ndarray", "class_name": "not_ndarray"})

    dense_no_names = {
        "type": "ndarray",
        "class_name": "ndarray",
        "data": np.array([1, 2, 3, 4], dtype=np.int32),
        "attributes": {"dim": {"type": "integer", "data": np.array([2, 2])}},
    }
    res_dense = _as_dense_matrix(dense_no_names)
    assert isinstance(res_dense, np.ndarray)
