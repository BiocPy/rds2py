# from functools import singledispatch
from importlib import import_module
from warnings import warn

from .rdsutils import get_class, parse_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

REGISTRY = {
    # typed vectors
    "integer_vector": "rds2py.read_atomic.parse_integer_vector",
    "boolean_vector": "rds2py.read_atomic.parse_boolean_vector",
    "string_vector": "rds2py.read_atomic.parse_string_vector",
    "double_vector": "rds2py.read_atomic.parse_double_vector",
    # dictionary
    "vector": "rds2py.read_dict.parse_dict",
    # factors
    "factor": "rds2py.read_factor.parse_factor",
    # Rle
    "Rle": "rds2py.read_rle.parse_rle",
    # matrices
    "dgCMatrix": "rds2py.read_matrix.parse_dgcmatrix",
    "dgRMatrix": "rds2py.read_matrix.parse_dgrmatrix",
    "dgTMatrix": "rds2py.read_matrix.parse_dgtmatrix",
    "ndarray": "rds2py.read_matrix.parse_ndarray",
    # data frames
    "data.frame": "rds2py.read_frame.parse_data_frame",
    "DFrame": "rds2py.read_frame.parse_dframe",
    # genomic ranges
    "GRanges": "rds2py.read_granges.parse_genomic_ranges",
    "GenomicRanges": "rds2py.read_granges.parse_genomic_ranges",
    "CompressedGRangesList": "rds2py.read_granges.parse_granges_list",
    "GRangesList": "rds2py.read_granges.parse_granges_list",
    # summarized experiment
    "SummarizedExperiment": "rds2py.read_se.parse_summarized_experiment",
    "RangedSummarizedExperiment": "rds2py.read_se.parse_ranged_summarized_experiment",
    # single-cell experiment
    "SingleCellExperiment": "rds2py.read_sce.parse_single_cell_experiment",
    "SummarizedExperimentByColumn": "rds2py.read_sce.parse_alts_summarized_experiment_by_column",
    # multi assay experiment
    "MultiAssayExperiment": "rds2py.read_mae.parse_multi_assay_experiment",
    "ExperimentList": "rds2py.read_dict.parse_dict",
}


# @singledispatch
# def save_rds(x, path: str):
#     """Save a Python object as RDS file.

#     Args:
#         x:
#             Object to save.

#         path:
#             Path to save the object.
#     """
#     raise NotImplementedError(
#         f"No `save_rds` method implemented for '{type(x).__name__}' objects."
#     )


def read_rds(path: str, **kwargs):
    """Read an RDS file as Python object.

    Args:
        path:
            Path to the RDS file.

        kwargs:
            Further arguments, passed to individual methods.

    Returns:
        Some kind of object.
    """
    _robj = parse_rds(path=path)
    return _dispatcher(_robj, **kwargs)


def _dispatcher(robject: dict, **kwargs):
    _class_name = get_class(robject)

    if _class_name is None:
        return None

    # if a class is registered, coerce the object
    # to the representation.
    if _class_name in REGISTRY:
        try:
            command = REGISTRY[_class_name]
            if isinstance(command, str):
                last_period = command.rfind(".")
                mod = import_module(command[:last_period])
                command = getattr(mod, command[last_period + 1 :])
                REGISTRY[_class_name] = command

            return command(robject, **kwargs)
        except Exception as e:
            warn(
                f"Failed to coerce RDS object to class: '{_class_name}', returning the dictionary, {str(e)}",
                RuntimeWarning,
            )
    else:
        warn(
            f"RDS file contains an unknown class: '{_class_name}', returning the dictionary",
            RuntimeWarning,
        )

    return robject
