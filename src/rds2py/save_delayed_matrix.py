from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("delayedarray", verbose=True):
    from delayedarray import DelayedArray

    @save_rds.register(DelayedArray)
    def _save_rds_delayedarray(x: DelayedArray, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()

            return getattr(obj, name, None)

        converted = {
            "type": "S4",
            "class_name": "H5SparseMatrix",
            "package_name": "HDF5Array",
            "attributes": {
                "seed": save_rds(_get(x, "seed")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted


if is_package_installed("hdf5array", verbose=True):
    from hdf5array import Hdf5CompressedSparseMatrixSeed

    @save_rds.register(Hdf5CompressedSparseMatrixSeed)
    def _save_rds_h5sparse_seed(x: Hdf5CompressedSparseMatrixSeed, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        converted = {
            "type": "S4",
            "class_name": "CSC_H5SparseMatrixSeed" if x.by_column else "CSR_H5SparseMatrixSeed",
            "package_name": "HDF5Array",
            "attributes": {
                "dim": save_rds(list(x.shape)),
                "filepath": save_rds([x.path]),
                "group": save_rds([x.group_name]),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
