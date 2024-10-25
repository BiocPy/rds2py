"""Core functionality for reading RDS files in Python.

This module provides the main interface for reading RDS files and converting them
to appropriate Python objects. It maintains a registry of supported R object types
and their corresponding Python parser functions.

The module supports various R object types including vectors, matrices, data frames,
and specialized Bioconductor objects like GenomicRanges and SummarizedExperiment.

Example:

    .. code-block:: python

        data = read_rds("example.rds")
        print(type(data))
"""

from importlib import import_module
from warnings import warn

from .rdsutils import get_class, parse_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

REGISTRY = {
    # typed vectors
    "integer_vector": "rds2py.read_atomic.read_integer_vector",
    "boolean_vector": "rds2py.read_atomic.read_boolean_vector",
    "string_vector": "rds2py.read_atomic.read_string_vector",
    "double_vector": "rds2py.read_atomic.read_double_vector",
    # dictionary
    "vector": "rds2py.read_dict.read_dict",
    # factors
    "factor": "rds2py.read_factor.read_factor",
    # Rle
    "Rle": "rds2py.read_rle.read_rle",
    # matrices
    "dgCMatrix": "rds2py.read_matrix.read_dgcmatrix",
    "dgRMatrix": "rds2py.read_matrix.read_dgrmatrix",
    "dgTMatrix": "rds2py.read_matrix.read_dgtmatrix",
    "ndarray": "rds2py.read_matrix.read_ndarray",
    # data frames
    "data.frame": "rds2py.read_frame.read_data_frame",
    "DFrame": "rds2py.read_frame.read_dframe",
    # genomic ranges
    "GRanges": "rds2py.read_granges.read_genomic_ranges",
    "GenomicRanges": "rds2py.read_granges.read_genomic_ranges",
    "CompressedGRangesList": "rds2py.read_granges.read_granges_list",
    "GRangesList": "rds2py.read_granges.read_granges_list",
    # summarized experiment
    "SummarizedExperiment": "rds2py.read_se.read_summarized_experiment",
    "RangedSummarizedExperiment": "rds2py.read_se.read_ranged_summarized_experiment",
    # single-cell experiment
    "SingleCellExperiment": "rds2py.read_sce.read_single_cell_experiment",
    "SummarizedExperimentByColumn": "rds2py.read_sce.read_alts_summarized_experiment_by_column",
    # multi assay experiment
    "MultiAssayExperiment": "rds2py.read_mae.read_multi_assay_experiment",
    "ExperimentList": "rds2py.read_dict.read_dict",
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
    """Read an RDS file and convert it to an appropriate Python object.

    Args:
        path:
            Path to the RDS file to be read.

        **kwargs:
            Additional arguments passed to specific parser functions.

    Returns:
        A Python object representing the data in the RDS file. The exact type
        depends on the contents of the RDS file and the available parsers.
    """
    _robj = parse_rds(path=path)
    return _dispatcher(_robj, **kwargs)


def _dispatcher(robject: dict, **kwargs):
    """Internal function to dispatch R objects to appropriate parser functions.

    Args:
        robject:
            Dictionary containing parsed R object data.

        **kwargs:
            Additional arguments passed to specific parser functions.

    Returns:
        Parsed Python object corresponding to the R data structure.
        Returns the original dictionary if no appropriate parser is found.
    """
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
