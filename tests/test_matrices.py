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
            "j": {"type": "integer", "data": np.array([0, 1])},
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

    dense_null_names = {
        "type": "ndarray",
        "class_name": "ndarray",
        "data": np.array([1, 2, 3, 4], dtype=np.int32),
        "attributes": {
            "dim": {"type": "integer", "class_name": "integer_vector", "data": np.array([2, 2])},
            "dimnames": {"type": "null"},
        },
    }
    res_null_names = _as_dense_matrix(dense_null_names)
    assert isinstance(res_null_names, np.ndarray)

    dgr_none_names = {
        "type": "S4",
        "class_name": "dgRMatrix",
        "attributes": {
            "x": {"type": "double", "class_name": "double_vector", "data": np.array([1.0, 2.0])},
            "j": {"type": "integer", "class_name": "integer_vector", "data": np.array([0, 1])},
            "p": {"type": "integer", "class_name": "integer_vector", "data": np.array([0, 1, 2])},
            "Dim": {"type": "integer", "class_name": "integer_vector", "data": np.array([2, 2])},
            "Dimnames": {
                "type": "vector",
                "class_name": "vector",
                "data": [{"type": "null"}, {"type": "null"}],
                "attributes": {},
            },
        },
    }
    res_dgr_none_names = _as_sparse_matrix(dgr_none_names)
    assert isinstance(res_dgr_none_names, sp.spmatrix)
    assert not isinstance(res_dgr_none_names, MatrixWrapper)

    dgr_null_names = {
        "type": "S4",
        "class_name": "dgRMatrix",
        "attributes": {
            "x": {"type": "double", "class_name": "double_vector", "data": np.array([1.0, 2.0])},
            "j": {"type": "integer", "class_name": "integer_vector", "data": np.array([0, 1])},
            "p": {"type": "integer", "class_name": "integer_vector", "data": np.array([0, 1, 2])},
            "Dim": {"type": "integer", "class_name": "integer_vector", "data": np.array([2, 2])},
            "Dimnames": {"type": "null"},
        },
    }
    res_dgr_null_names = _as_sparse_matrix(dgr_null_names)
    assert isinstance(res_dgr_null_names, sp.spmatrix)
    assert not isinstance(res_dgr_null_names, MatrixWrapper)

    from rds2py import save_rds

    wrapper_no_names = MatrixWrapper(np.array([[1, 2], [3, 4]]), dimnames=None)
    res_no_names = save_rds(wrapper_no_names)
    assert isinstance(res_no_names, dict)
    assert "dimnames" not in res_no_names["attributes"]


def test_save_sparse_matrices():
    import numpy as np
    from scipy import sparse as sp

    from rds2py import save_rds

    # CSC
    csc = sp.csc_matrix([[1, 0], [0, 2]], dtype=np.float64)
    res_csc = save_rds(csc)
    assert res_csc["type"] == "S4"
    assert res_csc["class_name"] == "dgCMatrix"
    assert res_csc["package_name"] == "Matrix"
    assert np.allclose(res_csc["attributes"]["x"], [1.0, 2.0])
    assert np.allclose(res_csc["attributes"]["i"], [0, 1])
    assert np.allclose(res_csc["attributes"]["p"], [0, 1, 2])

    # CSR
    csr = sp.csr_matrix([[1, 0], [0, 2]], dtype=np.float64)
    res_csr = save_rds(csr)
    assert res_csr["type"] == "S4"
    assert res_csr["class_name"] == "dgRMatrix"
    assert res_csr["package_name"] == "Matrix"
    assert np.allclose(res_csr["attributes"]["x"], [1.0, 2.0])
    assert np.allclose(res_csr["attributes"]["j"], [0, 1])
    assert np.allclose(res_csr["attributes"]["p"], [0, 1, 2])

    # COO
    coo = sp.coo_matrix([[1, 0], [0, 2]], dtype=np.float64)
    res_coo = save_rds(coo)
    assert res_coo["type"] == "S4"
    assert res_coo["class_name"] == "dgTMatrix"
    assert res_coo["package_name"] == "Matrix"
    assert np.allclose(res_coo["attributes"]["x"], [1.0, 2.0])
    assert np.allclose(res_coo["attributes"]["i"], [0, 1])
    assert np.allclose(res_coo["attributes"]["j"], [0, 1])

    # MatrixWrapper with Sparse Matrix and Dimnames
    wrapper = MatrixWrapper(csc, dimnames=[["r1", "r2"], ["c1", "c2"]])
    res_wrap = save_rds(wrapper)
    assert res_wrap["type"] == "S4"
    assert res_wrap["class_name"] == "dgCMatrix"
    assert "Dimnames" in res_wrap["attributes"]
    assert res_wrap["attributes"]["Dimnames"]["data"][0] == ["r1", "r2"]
    assert res_wrap["attributes"]["Dimnames"]["data"][1] == ["c1", "c2"]
