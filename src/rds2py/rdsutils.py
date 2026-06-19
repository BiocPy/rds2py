"""Utility functions for RDS/RData file parsing and class inference.

This module provides helper functions for parsing RDS and RData files and inferring the appropriate R class
information from parsed objects.
"""

from typing import Any, Dict, List, Optional

from .lib_rds_parser import write_rda as _write_rda_native
from .PyRdaReader import PyRdaParser
from .PyRdsReader import PyRdsParser

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_rds(path: str) -> dict:
    """Parse an RDS file into a dictionary representation.

    Args:
        path:
            Path to the RDS file to be parsed.

    Returns:
        A dictionary containing the parsed contents of the RDS file.
        The structure depends on the type of R object stored in the file.
    """
    parsed_obj = PyRdsParser(path)
    realized = parsed_obj.parse()

    return realized


def parse_rda(path: str, objects: Optional[List[str]] = None) -> Dict[str, dict]:
    """Parse an RData file into a dictionary of named objects.

    Args:
        path:
            Path to the RData (.RData/.rda) file to be parsed.

        objects:
            Optional list of object names to parse. If ``None``,
            all objects in the file are parsed.

    Returns:
        A dictionary mapping object names to their parsed representations.
        Each value has the same structure as the output of :py:func:`~.parse_rds`.
    """
    parser = PyRdaParser(path)

    if objects is None:
        return parser.parse()

    result = {}
    for name in objects:
        result[name] = parser.parse_object(name)
    return result


def write_rds(obj: Any, path: str) -> None:
    """Write a Python object to RDS file.

    Args:
        obj:
            The Python object to write.

        path:
            Output file path.
    """
    from .generics import save_rds

    save_rds(obj, path)


def write_rda(objects: Dict[str, Any], path: str) -> None:
    """Write multiple named Python objects to a gzip-compressed RData file.

    Each value is converted using :py:func:`~.write_rds`.

    Args:
        objects:
            Dictionary mapping variable names to Python objects.

        path:
            Output file path.
    """
    from .generics import save_rds

    converted = {str(k): save_rds(v) for k, v in objects.items()}
    _write_rda_native(converted, path)


def get_class(robj: dict) -> str:
    """Infer the R class name from a parsed RDS object.

    Notes:
        - Handles both S4 and non-S4 R objects
        - Special handling for vectors and matrices
        - Checks for class information in object attributes

    Args:
        robj:
            Dictionary containing parsed RDS data, typically
            the output of :py:func:`~.parse_rds`.

    Returns:
        The inferred R class name, or None if no class can be determined.
    """
    _inferred_cls_name = None
    if robj["type"] != "S4":
        if "class_name" in robj:
            _inferred_cls_name = robj["class_name"]
            if _inferred_cls_name is not None and (
                "integer" in _inferred_cls_name or "double" in _inferred_cls_name or _inferred_cls_name == "vector"
            ):
                if "attributes" in robj:
                    obj_attr = robj["attributes"]

                    # kind of making this assumption, if we ever see a dim, its a matrix
                    if obj_attr is not None:
                        if "dim" in obj_attr:
                            _inferred_cls_name = "ndarray"
                        elif "class" in obj_attr:
                            _inferred_cls_name = obj_attr["class"]["data"][0]

    else:
        _inferred_cls_name = robj["class_name"]

    return _inferred_cls_name
