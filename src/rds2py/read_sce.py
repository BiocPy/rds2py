"""Functions for parsing Bioconductor `SingleCellExperiment` objects.

This module provides parsers for converting Bioconductor's `SingleCellExperiment`
objects into their Python equivalents, handling the complex structure of single-cell
data including multiple assays, reduced dimensions, and alternative experiments.
"""

from singlecellexperiment import SingleCellExperiment

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_alts_summarized_experiment_by_column(robject: dict, **kwargs):
    """Parse alternative experiments in a SingleCellExperiment."""
    _cls = get_class(robject)

    if _cls not in ["SummarizedExperimentByColumn"]:
        raise RuntimeError(f"`robject` does not contain a 'SummarizedExperimentByColumn' object, contains `{_cls}`.")

    objs = {}

    for key, val in robject["attributes"].items():
        objs[key] = _dispatcher(val, **kwargs)

    return objs


def read_single_cell_experiment(robject: dict, **kwargs) -> SingleCellExperiment:
    """Convert an R SingleCellExperiment to Python SingleCellExperiment.

    Args:
        robject:
            Dictionary containing parsed SingleCellExperiment data.

        **kwargs:
            Additional arguments.

    Returns:
        A Python SingleCellExperiment object containing
        the assay data and associated metadata.
    """

    _cls = get_class(robject)

    if _cls not in ["SingleCellExperiment"]:
        raise RuntimeError(f"`robject` does not contain a 'SingleCellExperiment' object, contains `{_cls}`.")

    robject["class_name"] = "RangedSummarizedExperiment"
    _rse = _dispatcher(robject, **kwargs)

    # check red. dims, alternative expts
    robj_reduced_dims = None
    robj_alt_exps = None
    col_attrs = list(
        _dispatcher(robject["attributes"]["int_colData"]["attributes"]["listData"]["attributes"]["names"], **kwargs)
    )

    for idx in range(len(col_attrs)):
        idx_col = col_attrs[idx]
        idx_value = robject["attributes"]["int_colData"]["attributes"]["listData"]["data"][idx]

        if idx_col == "reducedDims" and idx_value.get("data", None) is not None:
            robj_reduced_dims = _dispatcher(idx_value, **kwargs)

        if idx_col == "altExps":
            alt_names = list(_dispatcher(idx_value["attributes"]["listData"]["attributes"]["names"], **kwargs))
            robj_alt_exps = {}
            for idx, altn in enumerate(alt_names):
                robj_alt_exps[altn] = _dispatcher(idx_value["attributes"]["listData"]["data"][idx], **kwargs)["se"]

        # ignore colpairs for now, does anyone even use this ?
        # if col == "colPairs":

    return SingleCellExperiment(
        assays=_rse.assays,
        row_data=_rse.row_data,
        column_data=_rse.column_data,
        row_ranges=_rse.row_ranges,
        alternative_experiments=robj_alt_exps,
        reduced_dims=robj_reduced_dims,
    )
