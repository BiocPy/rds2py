from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_rle(robject: dict):
    print("in parsing rle")
    data = list(_dispatcher(robject["attributes"]["values"]))

    if "lengths" in robject["attributes"]:
        lengths = _dispatcher(robject["attributes"]["lengths"])
    else:
        lengths = [1] * len(data)

    final_vec = []
    for i, x in enumerate(lengths):
        final_vec.extend([data[i]] * x)

    return final_vec
