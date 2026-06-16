"""Functions for saving atomic R vector types from Python objects."""

from typing import Optional

import numpy as np
from biocutils import BooleanList, FloatList, IntegerList, StringList

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register(bool)
@save_rds.register(int)
@save_rds.register(float)
@save_rds.register(str)
@save_rds.register(type(None))
def _save_rds_primitives(x, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    if path is not None:
        _write_rds_native(x, path)

    return x


@save_rds.register(BooleanList)
def _save_rds_booleanlist(x: BooleanList, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = np.array(list(x), dtype=bool)
    if path is not None:
        _write_rds_native(converted, path)

    return converted


@save_rds.register(IntegerList)
def _save_rds_integerlist(x: IntegerList, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = np.array(list(x), dtype=np.int32)
    if path is not None:
        _write_rds_native(converted, path)

    return converted


@save_rds.register(FloatList)
def _save_rds_floatlist(x: FloatList, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = np.array(list(x), dtype=np.float64)
    if path is not None:
        _write_rds_native(converted, path)

    return converted


@save_rds.register(StringList)
def _save_rds_stringlist(x: StringList, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = list(x)
    if path is not None:
        _write_rds_native(converted, path)

    return converted
