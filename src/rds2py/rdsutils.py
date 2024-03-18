from .core import PyParsedObject

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
    parsed_obj = PyParsedObject(path)
    robject_obj = parsed_obj.get_robject()
    realized = robject_obj.realize_value()

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