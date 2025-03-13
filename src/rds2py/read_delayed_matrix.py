"""Functions and classes for parsing R delayed matrix objects from HDF5Array."""

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_hdf5_sparse(robject: dict, **kwargs):
    """Convert an R delayed sparse array (H5-backed).

    Args:
        robject:
            Dictionary containing parsed delayed sparse array.

        **kwargs:
            Additional arguments.

    Returns:
       A Hdf5CompressedSparseMatrix from the 'hdf5array' package.
    """
    _cls = get_class(robject)
    if _cls not in ["H5SparseMatrix"]:
        raise RuntimeError(f"`robject` does not contain not a 'H5SparseMatrix' object, contains `{_cls}`.")

    by_column = False
    # get seed package name
    _seed_cls = get_class(robject["attributes"]["seed"])
    if _seed_cls in ["CSC_H5SparseMatrixSeed"]:
        by_column = True

    _seed_obj = robject["attributes"]["seed"]
    shape = tuple(_dispatcher(_seed_obj["attributes"]["dim"], **kwargs))
    fpath = list(_dispatcher(_seed_obj["attributes"]["filepath"], **kwargs))[0]
    group_name = list(_dispatcher(_seed_obj["attributes"]["group"], **kwargs))[0]

    from hdf5array import Hdf5CompressedSparseMatrix

    return Hdf5CompressedSparseMatrix(path=fpath, group_name=group_name, shape=shape, by_column=by_column)
