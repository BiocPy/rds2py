from typing import Optional

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


@save_rds.register(MatrixWrapper)
def _save_rds_matrixwrapper(x: MatrixWrapper, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = save_rds(x.matrix)

    if isinstance(converted, dict) and "attributes" in converted:
        if x.dimnames is not None:
            converted["attributes"]["dimnames"] = {
                "type": "vector",
                "data": [save_rds(list(names)) if names is not None else {"type": "null"} for names in x.dimnames],
            }

    if path is not None:
        _write_rds_native(converted, path)

    return converted
