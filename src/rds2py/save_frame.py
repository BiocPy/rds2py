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

        converted = {}
        for col_name in x.column_names:
            converted[col_name] = save_rds(x.column(col_name))

        if path is not None:
            _write_rds_native(converted, path)

        return converted
