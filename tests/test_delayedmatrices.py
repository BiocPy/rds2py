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
        assert isinstance(result, dict)
        assert list(result["class_name"]) == ["H5SparseMatrix"]
        assert list(result["package_name"]) == ["HDF5Array"]
        assert "attributes" in result

        seed = result["attributes"]["seed"]
        assert list(seed["class_name"]) == ["CSC_H5SparseMatrixSeed"]
        assert list(seed["package_name"]) == ["HDF5Array"]
        assert list(seed["attributes"]["group"]) == ["obsp/connectivities"]

    finally:
        if os.path.exists(h5_path):
            os.unlink(h5_path)
        if os.path.exists(rds_path):
            os.unlink(rds_path)
