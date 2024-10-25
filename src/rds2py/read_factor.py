"""Functions for parsing R factor objects.

This module handles the conversion of R factors (categorical variables) into Python lists, preserving the levels and
maintaining the order of the factor levels.
"""

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_factor(robject: dict, **kwargs) -> list:
    """Convert an R factor to a Python list.

    Args:
        robject:
            Dictionary containing parsed R factor data.

        **kwargs:
            Additional arguments.

    Returns:
        A list containing the factor values, with each value repeated
        according to its length if specified.
    """
    _cls = get_class(robject)

    if _cls not in ["factor"]:
        raise RuntimeError(f"`robject` does not contain not a factor object, contains `{_cls}`.")

    data = robject["data"]

    levels = None
    if "levels" in robject["attributes"]:
        levels = _dispatcher(robject["attributes"]["levels"], **kwargs)
    level_vec = [levels[x - 1] for x in data]

    if "lengths" in robject["attributes"]:
        lengths = _dispatcher(robject["attributes"]["lengths"], **kwargs)
    else:
        lengths = [1] * len(data)

    final_vec = []
    for i, x in enumerate(lengths):
        final_vec.extend([level_vec[i]] * x)

    return final_vec
