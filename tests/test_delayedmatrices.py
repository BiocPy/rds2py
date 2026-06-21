import os
import tempfile

import h5py
import numpy as np
from hdf5array import Hdf5CompressedSparseMatrix

from rds2py import read_rds, write_rds
from rds2py.generics import _dispatcher
from rds2py.rdsutils import parse_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_h5sparse():
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp_h5:
        h5_path = tmp_h5.name

    try:
        with h5py.File(h5_path, "w") as f:
            g = f.create_group("obsp/connectivities")
            g.create_dataset("data", data=np.ones(10, dtype=np.float64))
            g.create_dataset("indices", data=np.arange(10, dtype=np.int32))
            indptr = np.zeros(201, dtype=np.int32)
            indptr[-1] = 10
            g.create_dataset("indptr", data=indptr)

        robj = parse_rds("tests/data/h5sparse.rds")
        robj["attributes"]["seed"]["attributes"]["filepath"]["data"] = [h5_path]
        array = _dispatcher(robj)

        assert array is not None
        assert isinstance(array, Hdf5CompressedSparseMatrix)
        assert array.shape == (200, 200)

    finally:
        if os.path.exists(h5_path):
            os.unlink(h5_path)


def test_roundtrip_h5sparse():
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp_h5:
        h5_path = tmp_h5.name
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp_rds:
        rds_path = tmp_rds.name

    try:
        with h5py.File(h5_path, "w") as f:
            g = f.create_group("obsp/connectivities")
            g.create_dataset("data", data=np.array([1, 2, 3], dtype=np.float64))
            g.create_dataset("indices", data=np.array([0, 1, 2], dtype=np.int32))
            g.create_dataset("indptr", data=np.array([0, 1, 2, 3], dtype=np.int32))

        mat = Hdf5CompressedSparseMatrix(h5_path, "obsp/connectivities", (3, 3), True)
        write_rds(mat, rds_path)

        result = read_rds(rds_path)

        assert result is not None
        assert isinstance(result, Hdf5CompressedSparseMatrix)
        assert result.shape == (3, 3)
        assert result.group_name == "obsp/connectivities"

    finally:
        if os.path.exists(h5_path):
            os.unlink(h5_path)
        if os.path.exists(rds_path):
            os.unlink(rds_path)


def test_delayedarray_extra_branches_and_errors():
    import pytest
    from delayedarray import DelayedArray
    from hdf5array import Hdf5CompressedSparseMatrix

    from rds2py import save_rds
    from rds2py.read_delayed_matrix import read_hdf5_sparse

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp_h5:
        h5_path = tmp_h5.name
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp_rds:
        rds_path = tmp_rds.name

    try:
        with h5py.File(h5_path, "w") as f:
            g = f.create_group("obsp/connectivities")
            g.create_dataset("data", data=np.array([1, 2, 3], dtype=np.float64))
            g.create_dataset("indices", data=np.array([0, 1, 2], dtype=np.int32))
            g.create_dataset("indptr", data=np.array([0, 1, 2, 3], dtype=np.int32))

        mat = Hdf5CompressedSparseMatrix(h5_path, "obsp/connectivities", (3, 3), True)

        res = save_rds(mat)
        assert isinstance(res, dict)
        assert res["type"] == "S4"

        write_rds(mat.seed, rds_path)
        recreated_seed = read_rds(rds_path)
        assert recreated_seed is not None

        mat.get_seed = lambda: mat.seed
        try:
            res_hasattr = save_rds(mat)
            assert isinstance(res_hasattr, dict)
        finally:
            del mat.get_seed

        with pytest.raises(RuntimeError):
            read_hdf5_sparse({"type": "S4", "class_name": "BadClass"})

        csr_seed_mock = {
            "type": "S4",
            "class_name": "H5SparseMatrix",
            "attributes": {
                "seed": {
                    "type": "S4",
                    "class_name": "CSR_H5SparseMatrixSeed",
                    "attributes": {
                        "dim": {"type": "integer", "data": np.array([3, 3]), "class_name": "integer_vector"},
                        "filepath": {"type": "string", "data": [h5_path], "class_name": "string_vector"},
                        "group": {"type": "string", "data": ["obsp/connectivities"], "class_name": "string_vector"},
                    },
                }
            },
        }
        res_csr = read_hdf5_sparse(csr_seed_mock)
        assert isinstance(res_csr, Hdf5CompressedSparseMatrix)

    finally:
        if os.path.exists(h5_path):
            os.unlink(h5_path)
        if os.path.exists(rds_path):
            os.unlink(rds_path)
