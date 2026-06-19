from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("singlecellexperiment", verbose=True):
    from singlecellexperiment import SingleCellExperiment

    @save_rds.register(SingleCellExperiment)
    def _save_rds_sce(x: SingleCellExperiment, path: Optional[str] = None):
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
            "reduced_dims": save_rds(_get(x, "reduced_dims")),
            "main_experiment_name": save_rds(_get(x, "main_experiment_name")),
            "alternative_experiments": save_rds(_get(x, "alternative_experiments")),
            "row_pairs": save_rds(_get(x, "row_pairs")),
            "column_pairs": save_rds(_get(x, "column_pairs")),
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
