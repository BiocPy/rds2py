from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_rle(robject: dict):
    """Parse an Rle class as list.

    Args:
        robject:
            Object parsed from the `RDS` file.
            Usually the result of :py:func:`~rds2py.generics.read_rds`.

    Returns:
        List containing the Rle object.
    """
    _cls = get_class(robject)

    if _cls != "Rle":
        raise RuntimeError(f"`robject` does not contain a 'Rle' object, contains `{_cls}`.")

    data = list(_dispatcher(robject["attributes"]["values"]))

    if "lengths" in robject["attributes"]:
        lengths = _dispatcher(robject["attributes"]["lengths"])
    else:
        lengths = [1] * len(data)

    final_vec = []
    for i, x in enumerate(lengths):
        final_vec.extend([data[i]] * x)

    return final_vec
