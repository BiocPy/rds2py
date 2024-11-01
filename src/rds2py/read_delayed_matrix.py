"""Functions and classes for parsing R delayed matrix objects from HDF5Array."""

from typing import Literal

from hdf5array import Hdf5CompressedSparseMatrix

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_hdf5_sparse(robject: dict, **kwargs) -> Hdf5CompressedSparseMatrix:
    _cls = get_class(robject)

    if _cls not in ["H5SparseMatrix"]:
        raise RuntimeError(f"`robject` does not contain not a 'H5SparseMatrix' object, contains `{_cls}`.")

    by_column = False
    # get seed package name
    _seed_cls = get_class(robject["attributes"]["seed"])
    if _seed_cls in ["CSC_H5SparseMatrixSeed"]:
        by_column = True

    shape = _dispatcher(robject["attributes"]["seed"]["dim"], **kwargs)
    fpath = list(_dispatcher(robject["attributes"]["seed"]["filepath"], **kwargs))[0]
    group_name = list(_dispatcher(robject["attributes"]["seed"]["group"], **kwargs))[0]

    return Hdf5CompressedSparseMatrix(path=fpath, group_name=group_name, shape=shape, by_column=by_column)
