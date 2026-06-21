from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("summarizedexperiment", verbose=True):
    from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

    def _get_assay_dict(x):
        assays = x.get_assays() if hasattr(x, "get_assays") else getattr(x, "assays", {})
        if not assays:
            return None

        assay_names = list(assays.keys())
        assay_list_data = {
            "type": "vector",
            "data": [save_rds(v) for v in assays.values()],
            "attributes": {"names": {"type": "string", "data": assay_names}},
        }

        return {
            "type": "S4",
            "class_name": "SimpleAssays",
            "package_name": "SummarizedExperiment",
            "attributes": {
                "data": {
                    "type": "S4",
                    "class_name": "SimpleList",
                    "package_name": "S4Vectors",
                    "attributes": {
                        "listData": assay_list_data,
                        "elementType": {"type": "string", "data": ["ANY"]},
                        "elementMetadata": None,
                        "metadata": {"type": "vector", "data": []},
                    },
                }
            },
        }

    @save_rds.register(SummarizedExperiment)
    def _save_rds_se(x: SummarizedExperiment, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        converted = {
            "type": "S4",
            "class_name": "SummarizedExperiment",
            "package_name": "SummarizedExperiment",
            "attributes": {
                "assays": _get_assay_dict(x),
                "colData": save_rds(_get(x, "column_data")),
                "elementMetadata": save_rds(_get(x, "row_data")),
                "metadata": save_rds(_get(x, "metadata")),
                "NAMES": None,
            },
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
            "type": "S4",
            "class_name": "RangedSummarizedExperiment",
            "package_name": "SummarizedExperiment",
            "attributes": {
                "assays": _get_assay_dict(x),
                "colData": save_rds(_get(x, "column_data")),
                "elementMetadata": save_rds(_get(x, "row_data")),
                "metadata": save_rds(_get(x, "metadata")),
                "rowRanges": save_rds(_get(x, "row_ranges")),
                "NAMES": None,
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
