from typing import Optional

from biocutils import Factor

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register(Factor)
def _save_rds_factor(x: Factor, path: Optional[str] = None):
    from .lib_rds_parser import write_rds as _write_rds_native

    converted = {
        "type": "integer",
        "data": list(x.get_codes() + 1),
        "attributes": {
            "class": {"type": "string", "data": ["factor"]},
            "levels": {"type": "string", "data": list(x.get_levels())},
        },
    }

    if path is not None:
        _write_rds_native(converted, path)

    return converted
