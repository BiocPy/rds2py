from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("multiassayexperiment", verbose=True):
    from multiassayexperiment import MultiAssayExperiment

    @save_rds.register(MultiAssayExperiment)
    def _save_rds_mae(x: MultiAssayExperiment, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        expts = _get(x, "experiments")
        expts_list_data = {
            "type": "vector",
            "data": [save_rds(v) for v in expts.values()],
            "attributes": {"names": {"type": "string", "data": list(expts.keys())}},
        }
        expt_list_s4 = {
            "type": "S4",
            "class_name": "ExperimentList",
            "package_name": "MultiAssayExperiment",
            "attributes": {"listData": expts_list_data},
        }

        converted = {
            "type": "S4",
            "class_name": "MultiAssayExperiment",
            "package_name": "MultiAssayExperiment",
            "attributes": {
                "ExperimentList": expt_list_s4,
                "colData": save_rds(_get(x, "column_data")),
                "sampleMap": save_rds(_get(x, "sample_map")),
                "metadata": save_rds(_get(x, "metadata")),
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
