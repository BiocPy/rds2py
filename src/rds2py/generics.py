# from functools import singledispatch
from importlib import import_module
from warnings import warn

from .rdsutils import get_class, parse_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

REGISTRY = {
    # vectors
    "integer_vector": "rds2py.parse_integer_vector",
    "boolean_vector": "rds2py.parse_boolean_vector",
    "string_vector": "rds2py.parse_string_vector",
    "double_vector": "rds2py.parse_double_vector",
    "vector": "rds2py.parse_vector",
    # factors
    "factor": "rds2py.parse_factor",
    # Rle
    "Rle": "rds2py.parse_rle",
    # matrices
    "dgCMatrix": "rds2py.parse_dgcmatrix",
    "dgRMatrix": "rds2py.parse_dgrmatrix",
    "dgTMatrix": "rds2py.parse_dgtmatrix",
    "ndarray": "rds2py.parse_ndarray",
    # data frames
    "data.frame": "rds2py.parse_data_frame",
    "DFrame": "rds2py.parse_dframe",
    # genomic ranges
    "GRanges": "rds2py.parse_genomic_ranges",
    "GenomicRanges": "rds2py.parse_genomic_ranges",
    "CompressedGRangesList": "rds2py.parse_granges_list",
    "GRangesList": "rds2py.parse_granges_list",
    # summarized experiment
    "SummarizedExperiment": "rds2py.parse_summarized_experiment",
    "RangedSummarizedExperiment": "rds2py.parse_ranged_summarized_experiment",
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
    print("FULL OBJECT", _robj)
    return _dispatcher(_robj, **kwargs)


def _dispatcher(robject: dict, **kwargs):
    _class_name = get_class(robject)

    if _class_name is None:
        return None

    print("in READ_RDS")
    print(_class_name)
    # if a class is registered, coerce the object
    # to the representation.
    if _class_name in REGISTRY:
        # try:
        command = REGISTRY[_class_name]
        if isinstance(command, str):
            first_period = command.find(".")
            mod = import_module(command[:first_period])
            command = getattr(mod, command[first_period + 1 :])
            REGISTRY[_class_name] = command

        return command(robject, **kwargs)
        # except Exception as e:
        #     warn(
        #         f"Failed to coerce RDS object to class: '{_class_name}', returning the dictionary, {str(e)}",
        #         RuntimeWarning,
        #     )
    else:
        warn(
            f"RDS file contains an unknown class: '{_class_name}', returning the dictionary",
            UserWarning,
        )

    return robject
