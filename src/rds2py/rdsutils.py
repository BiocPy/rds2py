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
    is_integer = False
    if "class_name" in robj:
        if "integer" in robj["class_name"]:
            is_integer = True
        elif robj["class_name"] != "vector":
            return robj["class_name"]

    print(is_integer, "before")
    if "attributes" in robj:
        obj_attr = robj["attributes"]

        # kind of making this assumption, if we ever see a dim, its a matrix
        print(is_integer, obj_attr)
        if is_integer:
            if "dim" in obj_attr:
                return "ndarray"
            elif "class" in obj_attr: 
                return obj_attr["class"]["data"][0]
            else: 
                return robj["class_name"]

        if "class" in obj_attr:
            return obj_attr["class"]["data"][0]

    return None
