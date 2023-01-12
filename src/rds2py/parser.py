from .core import PyParsedObject

from typing import MutableMapping

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def read_rds(file: str) -> MutableMapping:
    """Read an RDS file as a python dict

    Args:
        file (str): Path to RDS file

    Returns:
        MutableMapping: realized R object as a python dict
    """
    parsed_obj = PyParsedObject(file)
    robject_obj = parsed_obj.get_robject()
    realized = robject_obj.realize_value()

    return realized


def get_class(robj: MutableMapping) -> str:
    """Generic method to get the class information of the realized R object

    Args:
        robj (MutableMapping): realized R object as dict

    Returns:
        str: class name
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
