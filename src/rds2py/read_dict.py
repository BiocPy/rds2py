"""Functions for parsing R vector and dictionary-like objects.

This module provides functionality to convert R named vectors and list objects into Python dictionaries or lists,
maintaining the structure and names of the original R objects.
"""

from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_dict(robject: dict, **kwargs) -> dict:
    """Convert an R named vector or list to a Python dictionary or list.

    Args:
        robject:
            Dictionary containing parsed R vector/list data.

        **kwargs:
            Additional arguments.

    Returns:
        If the R object has names, returns a dictionary mapping
        names to values. Otherwise, returns a list of parsed values.

    Example:
        >>> # For a named R vector c(a=1, b=2)
        >>> result = read_dict(robject)
        >>> print(result)
        {'a': 1, 'b': 2}
    """
    _cls = get_class(robject)

    if _cls not in ["vector"]:
        raise RuntimeError(f"`robject` does not contain not a vector/dictionary object, contains `{_cls}`.")

    if "names" not in robject["attributes"]:
        return [_dispatcher(x, **kwargs) for x in robject["data"]]

    dict_keys = list(_dispatcher(robject["attributes"]["names"], **kwargs))

    final_vec = {}
    for idx, dkey in enumerate(dict_keys):
        final_vec[dkey] = _dispatcher(robject["data"][idx], **kwargs)

    return final_vec
