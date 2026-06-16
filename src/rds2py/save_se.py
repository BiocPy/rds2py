from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("summarizedexperiment", verbose=True):
    from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

    @save_rds.register(SummarizedExperiment)
    def _save_rds_se(x: SummarizedExperiment, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "assays": save_rds(_get(x, "assays")),
            "row_data": save_rds(_get(x, "row_data")),
            "column_data": save_rds(_get(x, "column_data")),
            "metadata": save_rds(_get(x, "metadata")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted

    @save_rds.register(RangedSummarizedExperiment)
    def _save_rds_rse(x: RangedSummarizedExperiment, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "assays": save_rds(_get(x, "assays")),
            "row_data": save_rds(_get(x, "row_data")),
            "column_data": save_rds(_get(x, "column_data")),
            "row_ranges": save_rds(_get(x, "row_ranges")),
            "metadata": save_rds(_get(x, "metadata")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
