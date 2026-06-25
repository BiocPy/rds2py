from typing import Optional

import numpy as np
from biocutils.package_utils import is_package_installed
from numpy import ndarray

from .generics import save_rds
from .read_matrix import MatrixWrapper

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register(ndarray)
def _save_rds_ndarray(x: ndarray, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    x_flat = x.flatten(order="F") if x.ndim > 1 else x

    if x.ndim > 1:
        type_str = "double"
        if x.dtype.kind == "b":
            type_str = "logical"
        elif x.dtype.kind in "iu":
            type_str = "integer"

        converted = {
            "type": type_str,
            "data": x_flat,
            "attributes": {"dim": {"type": "integer", "data": list(x.shape)}},
        }
    else:
        converted = x_flat

    if path is not None:
        _write_rds_native(converted, path)

    return converted


if is_package_installed("scipy", verbose=True):
    from scipy.sparse import coo_matrix, csc_matrix, csr_matrix

    csc_classes = [csc_matrix]
    csr_classes = [csr_matrix]
    coo_classes = [coo_matrix]
    try:
        from scipy.sparse import coo_array, csc_array, csr_array

        csc_classes.append(csc_array)
        csr_classes.append(csr_array)
        coo_classes.append(coo_array)
    except ImportError:
        pass

    def _save_rds_csc(x, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        converted = {
            "type": "S4",
            "class_name": "dgCMatrix",
            "package_name": "Matrix",
            "attributes": {
                "i": x.indices.astype(np.int32, copy=False),
                "p": x.indptr.astype(np.int32, copy=False),
                "Dim": np.array(list(x.shape), dtype=np.int32),
                "Dimnames": {"type": "vector", "data": [{"type": "null"}, {"type": "null"}]},
                "x": x.data.astype(np.float64, copy=False),
                "factors": {"type": "vector", "data": []},
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    for cls in csc_classes:
        save_rds.register(cls, _save_rds_csc)

    def _save_rds_csr(x, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        converted = {
            "type": "S4",
            "class_name": "dgRMatrix",
            "package_name": "Matrix",
            "attributes": {
                "j": x.indices.astype(np.int32, copy=False),
                "p": x.indptr.astype(np.int32, copy=False),
                "Dim": np.array(list(x.shape), dtype=np.int32),
                "Dimnames": {"type": "vector", "data": [{"type": "null"}, {"type": "null"}]},
                "x": x.data.astype(np.float64, copy=False),
                "factors": {"type": "vector", "data": []},
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    for cls in csr_classes:
        save_rds.register(cls, _save_rds_csr)

    def _save_rds_coo(x, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        converted = {
            "type": "S4",
            "class_name": "dgTMatrix",
            "package_name": "Matrix",
            "attributes": {
                "i": x.row.astype(np.int32, copy=False),
                "j": x.col.astype(np.int32, copy=False),
                "Dim": np.array(list(x.shape), dtype=np.int32),
                "Dimnames": {"type": "vector", "data": [{"type": "null"}, {"type": "null"}]},
                "x": x.data.astype(np.float64, copy=False),
                "factors": {"type": "vector", "data": []},
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    for cls in coo_classes:
        save_rds.register(cls, _save_rds_coo)


@save_rds.register(MatrixWrapper)
def _save_rds_matrixwrapper(x: MatrixWrapper, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = save_rds(x.matrix)

    if isinstance(converted, dict) and "attributes" in converted:
        if x.dimnames is not None:
            key = "Dimnames" if converted.get("type") == "S4" else "dimnames"
            converted["attributes"][key] = {
                "type": "vector",
                "data": [save_rds(list(names)) if names is not None else {"type": "null"} for names in x.dimnames],
            }

    if path is not None:
        _write_rds_native(converted, path)

    return converted
