from typing import Optional

from numpy import ndarray

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register(ndarray)
def _save_rds_ndarray(x: ndarray, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    x_flat = x.flatten(order="F") if x.ndim > 1 else x
    if path is not None:
        _write_rds_native(x_flat, path)

    return x_flat
