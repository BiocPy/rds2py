from .PyRdsReader import PyRdsParser

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_rds(path: str) -> dict:
    """Parse an RDS file as a :py:class:`~dict`.

    Args:
        path:
            Path to RDS file.

    Returns:
        A dictionary with the contents of the RDS file.
    """
    parsed_obj = PyRdsParser(path)
    realized = parsed_obj.parse()

    return realized


def get_class(robj: dict) -> str:
    """Guess class information of the R object.

    Args:
        robj:
            Object parsed from the `RDS` file.
            Usually the result of :py:func:`~rds2py.parser.load_rds`.

    Returns:
        A string representing the class name from R.
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
