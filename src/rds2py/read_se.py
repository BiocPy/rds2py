from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

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


def read_summarized_experiment(robject: dict, **kwargs) -> SummarizedExperiment:
    """Convert an R SummarizedExperiment to Python
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`.

    Args:
        robject:
            Dictionary containing parsed SummarizedExperiment data.

        **kwargs:
            Additional arguments.

    Returns:
        A `SummarizedExperiment` from the R object.
    """

    _cls = get_class(robject)

    if _cls not in ["SummarizedExperiment"]:
        raise RuntimeError(f"`robject` does not contain a 'SummarizedExperiment' object, contains `{_cls}`.")
    # parse assays  names
    robj_asys = {}
    assay_dims = None
    asy_names = list(
        _dispatcher(
            robject["attributes"]["assays"]["attributes"]["data"]["attributes"]["listData"]["attributes"]["names"],
            **kwargs,
        )
    )
    for idx, asyname in enumerate(asy_names):
        idx_asy = robject["attributes"]["assays"]["attributes"]["data"]["attributes"]["listData"]["data"][idx]

        robj_asys[asyname] = _dispatcher(idx_asy, **kwargs)
        if assay_dims is None:
            assay_dims = robj_asys[asyname].shape

    # parse coldata
    robj_coldata = _sanitize_empty_frame(_dispatcher(robject["attributes"]["colData"], **kwargs), assay_dims[1])

    # parse rowdata
    robj_rowdata = _sanitize_empty_frame(_dispatcher(robject["attributes"]["elementMetadata"], **kwargs), assay_dims[0])

    return SummarizedExperiment(
        assays=_sanitize_assays(robj_asys),
        row_data=robj_rowdata,
        column_data=robj_coldata,
    )


def read_ranged_summarized_experiment(robject: dict, **kwargs) -> RangedSummarizedExperiment:
    """Convert an R RangedSummarizedExperiment to its Python equivalent.

    Args:
        robject:
            Dictionary containing parsed SummarizedExperiment data.

        **kwargs:
            Additional arguments.

    Returns:
        A Python RangedSummarizedExperiment object.
    """

    _cls = get_class(robject)

    if _cls not in ["RangedSummarizedExperiment"]:
        raise RuntimeError(f"`robject` does not contain a 'RangedSummarizedExperiment' object, contains `{_cls}`.")

    robject["class_name"] = "SummarizedExperiment"
    _se = _dispatcher(robject, **kwargs)

    # parse rowRanges
    row_ranges_data = None
    if "rowRanges" in robject["attributes"]:
        row_ranges_data = _dispatcher(robject["attributes"]["rowRanges"], **kwargs)

    return RangedSummarizedExperiment(
        assays=_se.assays,
        row_data=_se.row_data,
        column_data=_se.column_data,
        row_ranges=row_ranges_data,
    )
