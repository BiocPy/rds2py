from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("iranges", verbose=True):
    from iranges import IRanges

    @save_rds.register(IRanges)
    def _save_rds_iranges(x: IRanges, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "type": "S4",
            "class_name": "IRanges",
            "package_name": "IRanges",
            "attributes": {
                "start": save_rds(_get(x, "start")),
                "width": save_rds(_get(x, "width")),
                "NAMES": save_rds(_get(x, "names")),
                "elementType": {"type": "string", "data": ["ANY"]},
                "elementMetadata": save_rds(_get(x, "mcols")),
                "metadata": save_rds(_get(x, "metadata")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
