from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_single_cell_experiment(robject: dict):
    """Parse an R object as :py:class:`~singlecellexperiment.SingleCellExperiment.SingleCellExperiment`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A `SingleCellExperiment` from the R object.
    """
    from singlecellexperiment import SingleCellExperiment

    _cls = get_class(robject)

    if _cls not in ["SingleCellExperiment"]:
        raise RuntimeError(
            f"`robject` does not contain a 'SingleCellExperiment' object, contains `{_cls}`."
        )

    robject["class_name"] = "RangedSummarizedExperiment"
    _rse = _dispatcher(robject)

    # check red. dims, alternative expts
    robj_reduced_dims = None
    robj_altExps = None
    col_attrs = list(_dispatcher(robject["attributes"]["int_colData"]["attributes"]["listData"]["attributes"]["names"]))

    for idx in range(len(col_attrs)):
        idx_col = col_attrs[idx]
        idx_value = robject["attributes"]["int_colData"]["attributes"]["listData"][
            "data"
        ][idx]

        if idx_col == "reducedDims" and idx_value["data"] is not None:
            robj_reduced_dims = _dispatcher(idx_value)

        if idx_col == "altExps":
            alt_names = idx_value["attributes"]["listData"]["attributes"]["names"][
                "data"
            ]
            robj_altExps = {}
            for idx_alt_names in range(len(alt_names)):
                altn = alt_names[idx_alt_names]

                alt_key = list(
                    idx_value["attributes"]["listData"]["data"][idx_alt_names][
                        "attributes"
                    ].keys()
                )[0]

                robj_altExps[altn] = _dispatcher(
                    idx_value["attributes"]["listData"]["data"][idx_alt_names][
                        "attributes"
                    ][alt_key]
                )

        # ignore colpairs for now, does anyone even use this ?
        # if col == "colPairs":

    return SingleCellExperiment(
        assays=_rse.assays,
        row_data=_rse.row_data,
        column_data=_rse.column_data,
        row_ranges=_rse.row_ranges,
        alternative_experiments=robj_altExps,
        reduced_dims=robj_reduced_dims,
    )
