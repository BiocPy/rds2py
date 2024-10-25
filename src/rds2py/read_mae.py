"""Functions for parsing Bioconductor MultiAssayExperiment objects.

This module handles the conversion of Bioconductor's MultiAssayExperiment container format into its Python equivalent,
preserving the complex relationships between multiple experimental assays and sample metadata.
"""

from multiassayexperiment import MultiAssayExperiment

from .generics import _dispatcher
from .rdsutils import get_class
from .read_matrix import MatrixWrapper

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _sanitize_expts(expts, **kwargs):
    """Convert raw experiment objects into SummarizedExperiment format.

    Args:
        expts:
            Dictionary of experiment objects.

    Returns:
        Dictionary of converted experiments, with matrix-like objects
        wrapped in SummarizedExperiment containers.
    """
    from biocframe import BiocFrame
    from summarizedexperiment import SummarizedExperiment

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


def read_multi_assay_experiment(robject: dict, **kwargs) -> MultiAssayExperiment:
    """Convert an R `MultiAssayExperiment` to a Python :py:class:`~multiassayexperiment.MultiAssayExperiment` object.

    Args:
        robject:
            Dictionary containing parsed MultiAssayExperiment data.

        **kwargs:
            Additional arguments.

    Returns:
        A Python `MultiAssayExperiment` object containing
        multiple experimental assays with associated metadata.
    """

    _cls = get_class(robject)

    if _cls not in ["MultiAssayExperiment"]:
        raise RuntimeError(f"`robject` does not contain a 'MultiAssayExperiment' object, contains `{_cls}`.")

    # parse experiment  names
    _expt_obj = robject["attributes"]["ExperimentList"]["attributes"]["listData"]
    robj_expts = _dispatcher(_expt_obj, **kwargs)

    # parse sample_map
    robj_samplemap = _dispatcher(robject["attributes"]["sampleMap"], **kwargs)

    # parse coldata
    robj_coldata = _dispatcher(robject["attributes"]["colData"], **kwargs)

    return MultiAssayExperiment(
        experiments=_sanitize_expts(robj_expts),
        sample_map=robj_samplemap,
        column_data=robj_coldata,
    )
