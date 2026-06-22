from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("biocframe", verbose=True):
    from biocframe import BiocFrame

    @save_rds.register(BiocFrame)
    def _save_rds_biocframe(x: BiocFrame, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        list_data = {
            "type": "vector",
            "data": [save_rds(x.column(col_name)) for col_name in x.column_names],
            "attributes": {"names": {"type": "string", "data": list(x.column_names)}},
        }

        rownames = x.row_names
        if rownames is not None:
            rownames_data = {"type": "string", "data": list(rownames)}
        else:
            rownames_data = {"type": "null"}

        converted = {
            "type": "S4",
            "class_name": "DFrame",
            "package_name": "S4Vectors",
            "attributes": {
                "listData": list_data,
                "rownames": rownames_data,
                "nrows": {"type": "integer", "data": [x.shape[0]]},
                "elementType": {"type": "string", "data": ["ANY"]},
                "elementMetadata": {"type": "null"},
                "metadata": {"type": "vector", "data": []},
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
