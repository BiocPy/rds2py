"""Functions for parsing atomic R vector types into Python objects.

This module provides parser functions for converting R's atomic vector types (boolean, integer, string, and double) into
appropriate Python objects using the biocutils package's specialized list classes.
"""

from biocutils import BooleanList, FloatList, IntegerList, StringList

from .generics import _dispatcher

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def _extract_names(robject: dict, **kwargs):
    """Extract names attribute from an R object if present.

    Args:
        robject:
            Dictionary containing parsed R object data.

        **kwargs:
            Additional arguments.

    Returns:
        List of names if present in the object's attributes,
        None otherwise.
    """
    _names = None
    if "attributes" in robject and robject["attributes"] is not None:
        if "names" in robject["attributes"]:
            _names = _dispatcher(robject["attributes"]["names"])

    return _names


def read_boolean_vector(robject: dict, **kwargs) -> BooleanList:
    """Convert an R boolean vector to a Python :py:class:`~biocutils.BooleanList`.

    Args:
        robject:
            Dictionary containing parsed R boolean vector data.

        **kwargs:
            Additional arguments.

    Returns:
        A `BooleanList` object containing the vector data
        and any associated names.
    """
    _names = _extract_names(robject, **kwargs)

    obj = BooleanList(robject["data"], names=_names)
    return obj


def read_integer_vector(robject: dict, **kwargs) -> IntegerList:
    """Convert an R integer vector to a Python :py:class:`~biocutils.IntegerList`.

    Args:
        robject:
            Dictionary containing parsed R integer vector data.

        **kwargs:
            Additional arguments.

    Returns:
        A `IntegerList` object containing the vector data
        and any associated names.
    """
    _names = _extract_names(robject, **kwargs)

    obj = IntegerList(robject["data"], names=_names)
    return obj


def read_string_vector(robject: dict, **kwargs) -> StringList:
    """Convert an R string vector to a Python :py:class:`~biocutils.StringList`.

    Args:
        robject:
            Dictionary containing parsed R string vector data.

        **kwargs:
            Additional arguments.

    Returns:
        A `StringList` object containing the vector data
        and any associated names.
    """
    _names = _extract_names(robject, **kwargs)

    obj = StringList(robject["data"], names=_names)
    return obj


def read_double_vector(robject: dict, **kwargs) -> FloatList:
    """Convert an R double vector to a Python :py:class:`~biocutils.FloatList`.

    Args:
        robject:
            Dictionary containing parsed R double vector data.

        **kwargs:
            Additional arguments.

    Returns:
        A `FloatList` object containing the vector data
        and any associated names.
    """
    _names = _extract_names(robject, **kwargs)

    obj = FloatList(robject["data"], names=_names)
    return obj
