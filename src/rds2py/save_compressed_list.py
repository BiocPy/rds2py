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

        class_name = type(x).__name__
        r_class_name = class_name
        element_type = "ANY"
        if class_name == "CompressedIntegerList":
            element_type = "integer"
        elif class_name == "CompressedCharacterList":
            element_type = "character"
        elif class_name == "CompressedBooleanList":
            r_class_name = "CompressedLogicalList"
            element_type = "logical"
        elif class_name == "CompressedFloatList":
            r_class_name = "CompressedNumericList"
            element_type = "numeric"
        elif class_name == "CompressedSplitBiocFrameList":
            r_class_name = "CompressedSplitDFrameList"
            element_type = "DFrame"

        converted = {
            "type": "S4",
            "class_name": r_class_name,
            "package_name": "IRanges",
            "attributes": {
                "unlistData": save_rds(_get(x, "unlist_data")),
                "partitioning": save_rds(_get(x, "partitioning")),
                "elementType": {"type": "string", "data": [element_type]},
                "elementMetadata": save_rds(_get(x, "element_metadata")),
                "metadata": save_rds(_get(x, "metadata")),
            },
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
            "type": "S4",
            "class_name": "PartitioningByEnd",
            "package_name": "IRanges",
            "attributes": {
                "end": save_rds(_get(x, "ends")),
                "NAMES": save_rds(_get(x, "names")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
