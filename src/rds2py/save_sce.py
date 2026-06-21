from typing import Optional

from biocutils.package_utils import is_package_installed

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


if is_package_installed("singlecellexperiment", verbose=True):
    from singlecellexperiment import SingleCellExperiment

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

    @save_rds.register(SingleCellExperiment)
    def _save_rds_sce(x: SingleCellExperiment, path: Optional[str] = None):
        from .lib_rds_parser import write_rds as _write_rds_native

        def _get(obj, name):
            if hasattr(obj, f"get_{name}"):
                return getattr(obj, f"get_{name}")()
            return getattr(obj, name, None)

        def _make_internal_dframe(list_data, nrows):
            return {
                "type": "S4",
                "class_name": "DFrame",
                "package_name": "S4Vectors",
                "attributes": {
                    "listData": list_data,
                    "rownames": {"type": "null"},
                    "nrows": {"type": "integer", "data": [nrows]},
                    "elementType": {"type": "string", "data": ["ANY"]},
                    "elementMetadata": {"type": "null"},
                    "metadata": {"type": "vector", "data": []},
                },
            }

        int_list_data = {"type": "vector", "data": [], "attributes": {"names": {"type": "string", "data": []}}}

        reduced_dims = _get(x, "reduced_dims")
        if reduced_dims is not None and len(reduced_dims) > 0:
            red_dims_list_data = {
                "type": "vector",
                "data": [save_rds(v) for v in reduced_dims.values()],
                "attributes": {"names": {"type": "string", "data": list(reduced_dims.keys())}},
            }
            red_dims_converted = _make_internal_dframe(red_dims_list_data, x.shape[1])
        else:
            red_dims_converted = _make_internal_dframe(
                {"type": "vector", "data": [], "attributes": {"names": {"type": "string", "data": []}}}, x.shape[1]
            )

        int_list_data["data"].append(red_dims_converted)
        int_list_data["attributes"]["names"]["data"].append("reducedDims")

        alt_exps = _get(x, "alternative_experiments")
        if alt_exps is not None and len(alt_exps) > 0:
            alt_exps_list_data = {
                "type": "vector",
                "data": [],
                "attributes": {"names": {"type": "string", "data": list(alt_exps.keys())}},
            }
            for k, v in alt_exps.items():
                alt_exps_list_data["data"].append(
                    {
                        "type": "S4",
                        "class_name": "SummarizedExperimentByColumn",
                        "package_name": "SingleCellExperiment",
                        "attributes": {"se": save_rds(v)},
                    }
                )
            alt_exps_converted = _make_internal_dframe(alt_exps_list_data, x.shape[1])
        else:
            alt_exps_converted = _make_internal_dframe(
                {"type": "vector", "data": [], "attributes": {"names": {"type": "string", "data": []}}}, x.shape[1]
            )

        int_list_data["data"].append(alt_exps_converted)
        int_list_data["attributes"]["names"]["data"].append("altExps")

        col_pairs_converted = _make_internal_dframe(
            {"type": "vector", "data": [], "attributes": {"names": {"type": "string", "data": []}}}, x.shape[1]
        )
        int_list_data["data"].append(col_pairs_converted)
        int_list_data["attributes"]["names"]["data"].append("colPairs")

        int_coldata = {
            "type": "S4",
            "class_name": "DFrame",
            "package_name": "S4Vectors",
            "attributes": {
                "listData": int_list_data,
                "rownames": {"type": "null"},
                "nrows": {"type": "integer", "data": [x.shape[1]]},
                "elementType": {"type": "string", "data": ["ANY"]},
                "elementMetadata": {"type": "null"},
                "metadata": {"type": "vector", "data": []},
            },
        }

        row_pairs_converted = _make_internal_dframe(
            {"type": "vector", "data": [], "attributes": {"names": {"type": "string", "data": []}}}, x.shape[0]
        )

        int_elementMetadata_list_data = {
            "type": "vector",
            "data": [row_pairs_converted],
            "attributes": {"names": {"type": "string", "data": ["rowPairs"]}},
        }

        int_elementMetadata = _make_internal_dframe(int_elementMetadata_list_data, x.shape[0])

        version_obj = {
            "type": "vector",
            "data": [{"type": "integer", "data": [99, 99, 99]}],
            "attributes": {"class": {"type": "string", "data": ["package_version", "numeric_version"]}},
        }

        int_metadata = {
            "type": "vector",
            "data": [version_obj],
            "attributes": {"names": {"type": "string", "data": ["version"]}},
        }

        converted = {
            "type": "S4",
            "class_name": "SingleCellExperiment",
            "package_name": "SingleCellExperiment",
            "attributes": {
                "assays": _get_assay_dict(x),
                "colData": save_rds(_get(x, "column_data")),
                "elementMetadata": save_rds(_get(x, "row_data")),
                "metadata": save_rds(_get(x, "metadata")),
                "rowRanges": save_rds(_get(x, "row_ranges")),
                "int_colData": int_coldata,
                "int_elementMetadata": int_elementMetadata,
                "int_metadata": int_metadata,
                "NAMES": None,
            },
        }

        if path is not None:
            _write_rds_native(converted, path)

        return converted
