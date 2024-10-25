from .generics import _dispatcher
from .rdsutils import get_class

from .read_matrix import MatrixWrapper

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _sanitize_empty_frame(frame, nrows):
    if frame.shape == (0, 0):
        from biocframe import BiocFrame

        return BiocFrame(number_of_rows=nrows)

def _sanitize_assays(assays):
    res = {}
    for k, v in assays.items():
        if isinstance(v, MatrixWrapper):
            res[k] = v.matrix
        else:
                res[k] = v

    return res

def parse_summarized_experiment(robject: dict):
    """Parse an R object as :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A `SummarizedExperiment` from the R object.
    """
    from summarizedexperiment import SummarizedExperiment

    _cls = get_class(robject)

    if _cls not in ["SummarizedExperiment"]:
        raise RuntimeError(
            f"`robject` does not contain a 'SummarizedExperiment' object, contains `{_cls}`."
        )
    # parse assays  names
    robj_asys = {}
    assay_dims = None
    asy_names = list(
        _dispatcher(
            robject["attributes"]["assays"]["attributes"]["data"]["attributes"][
                "listData"
            ]["attributes"]["names"]
        )
    )
    for idx, asyname in enumerate(asy_names):
        idx_asy = robject["attributes"]["assays"]["attributes"]["data"]["attributes"][
            "listData"
        ]["data"][idx]

        robj_asys[asyname] = _dispatcher(idx_asy)
        if assay_dims is None:
            assay_dims = robj_asys[asyname].shape

    # parse coldata
    robj_coldata = _sanitize_empty_frame(
        _dispatcher(robject["attributes"]["colData"]), assay_dims[1]
    )

    # parse rowdata
    robj_rowdata = _sanitize_empty_frame(
        _dispatcher(robject["attributes"]["elementMetadata"]), assay_dims[0]
    )

    return SummarizedExperiment(
        assays=_sanitize_assays(robj_asys), row_data=robj_rowdata, column_data=robj_coldata
    )


def parse_ranged_summarized_experiment(robject: dict):
    """Parse an R object as :py:class:`~summarizedexperiment.SummarizedExperiment.RangedSummarizedExperiment`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A `RangedSummarizedExperiment` from the R object.
    """
    from summarizedexperiment import RangedSummarizedExperiment

    _cls = get_class(robject)

    if _cls not in ["RangedSummarizedExperiment"]:
        raise RuntimeError(
            f"`robject` does not contain a 'RangedSummarizedExperiment' object, contains `{_cls}`."
        )

    robject["class_name"] = "SummarizedExperiment"
    _se = _dispatcher(robject)

    # parse rowRanges
    row_ranges_data = None
    if "rowRanges" in robject["attributes"]:
        row_ranges_data = _dispatcher(robject["attributes"]["rowRanges"])

    return RangedSummarizedExperiment(
        assays=_se.assays,
        row_data=_se.row_data,
        column_data=_se.column_data,
        row_ranges=row_ranges_data,
    )
