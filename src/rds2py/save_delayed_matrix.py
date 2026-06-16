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
            "seed": save_rds(_get(x, "seed")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
