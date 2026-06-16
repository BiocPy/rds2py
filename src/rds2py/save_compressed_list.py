"""Functions and classes for parsing Compressed List data structures."""

from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

if is_package_installed("compressed_lists", verbose=True):
    from compressed_lists import CompressedList, Partitioning

    @save_rds.register(CompressedList)
    def _save_rds_compressedlist(x: CompressedList, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "unlist_data": save_rds(_get(x, "unlist_data")),
            "partitioning": save_rds(_get(x, "partitioning")),
            "metadata": save_rds(_get(x, "metadata")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    @save_rds.register(Partitioning)
    def _save_rds_partitioning(x: Partitioning, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "ends": save_rds(_get(x, "ends")),
            "names": save_rds(_get(x, "names")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
