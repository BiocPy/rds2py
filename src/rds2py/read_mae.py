from .generics import _dispatcher
from .rdsutils import get_class

from .read_matrix import MatrixWrapper


__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _sanitize_expts(expts):
    from summarizedexperiment import SummarizedExperiment
    from biocframe import BiocFrame

    res = {}
    for k, v in expts.items():
        if isinstance(v, MatrixWrapper):
            res[k] = SummarizedExperiment(
                assays={"matrix": v.matrix},
                row_data=BiocFrame(row_names=v.dimnames[0]),
                column_data=BiocFrame(row_names=v.dimnames[1]),
            )
        else:
            res[k] = v

    return res


def parse_multi_assay_experiment(robject: dict):
    """Parse an R object as :py:class:`~multiassayexperiment.MultiAssayExperiment.MultiAssayExperiment`.

    Args:
        robject:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        A `MultiAssayExperiment` from the R object.
    """
    from multiassayexperiment import MultiAssayExperiment

    _cls = get_class(robject)

    if _cls not in ["MultiAssayExperiment"]:
        raise RuntimeError(
            f"`robject` does not contain a 'MultiAssayExperiment' object, contains `{_cls}`."
        )

    # parse experiment  names
    _expt_obj = robject["attributes"]["ExperimentList"]["attributes"]["listData"]
    robj_expts = _dispatcher(_expt_obj)

    # parse sample_map
    robj_samplemap = _dispatcher(robject["attributes"]["sampleMap"])

    # parse coldata
    robj_coldata = _dispatcher(robject["attributes"]["colData"])

    return MultiAssayExperiment(
        experiments=_sanitize_expts(robj_expts),
        sample_map=robj_samplemap,
        column_data=robj_coldata,
    )
