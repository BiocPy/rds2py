from typing import Optional

from biocutils import NamedList

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register(dict)
def _save_rds_dict(x: dict, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = {str(k): save_rds(v) for k, v in x.items()}
    if path is not None:
        _write_rds_native(converted, path)

    return converted


@save_rds.register(list)
@save_rds.register(tuple)
def _save_rds_list(x, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = [save_rds(v) for v in x]
    if path is not None:
        _write_rds_native(converted, path)

    return converted


@save_rds.register(NamedList)
def _save_rds_namedlist(x: NamedList, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = {str(k): save_rds(v) for k, v in x.items()}
    if path is not None:
        _write_rds_native(converted, path)

    return converted
