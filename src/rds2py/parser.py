from typing import Dict, MutableMapping

from .core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_rds(file: str) -> Dict:
    """Read an RDS file as a :py:class:`~dict`.

    Args:
        file (str): Path to RDS file.

    Returns:
        MutableMapping: R object as a python dictionary.
    """
    parsed_obj = PyParsedObject(file)
    robject_obj = parsed_obj.get_robject()
    realized = robject_obj.realize_value()

    return realized


def get_class(robj: MutableMapping) -> str:
    """Generic method to get the class information of the R object.

    Args:
        robj (MutableMapping): Object parsed from the `RDS` file.
            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        str: Class name.
    """
    if "class_name" in robj:
        return robj["class_name"]

    if "attributes" in robj and len(robj["attributes"].keys()) > 0:
        obj_attr = robj["attributes"]
        if "class" in obj_attr:
            return obj_attr["class"]["data"][0]

        # kind of making this assumption, if we ever see a dim, its a matrix
        if "dim" in obj_attr:
            return "densematrix"

    return None
