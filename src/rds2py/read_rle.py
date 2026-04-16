"""Functions for parsing R's Rle (Run-length encoding) objects.

This module provides functionality to convert R's Rle (Run-length encoding) objects into Python lists, expanding the
compressed representation into its full form.
"""

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_rle(robject: dict, **kwargs) -> list:
    """Convert an R Rle object to a Python list.

    Args:
        robject:
            Dictionary containing parsed Rle data.

        **kwargs:
            Additional arguments.

    Returns:
        Expanded list where each value is repeated according to its run length.

    Example:
        >>> # For Rle with values=[1,2] and lengths=[3,2]
        >>> result = read_rle(robject)
        >>> print(result)
        [1, 1, 1, 2, 2]
    """
    _cls = get_class(robject)

    if _cls != "Rle":
        raise RuntimeError(f"`robject` does not contain a 'Rle' object, contains `{_cls}`.")

    data = list(_dispatcher(robject["attributes"]["values"], **kwargs))

    if "lengths" in robject["attributes"]:
        lengths = _dispatcher(robject["attributes"]["lengths"], **kwargs)
    else:
        lengths = [1] * len(data)

    final_vec = []
    for i, x in enumerate(lengths):
        final_vec.extend([data[i]] * x)

    return final_vec
