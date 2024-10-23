from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_factor(robject: dict):
    _cls = get_class(robject)

    if _cls not in ["factor"]:
        raise RuntimeError(f"`robject` does not contain not a factor object, contains `{_cls}`.")

    data = robject["data"]

    levels = None
    if "levels" in robject["attributes"]:
        levels = _dispatcher(robject["attributes"]["levels"])
    level_vec = [levels[x - 1] for x in data]

    if "lengths" in robject["attributes"]:
        lengths = _dispatcher(robject["attributes"]["lengths"])
    else:
        lengths = [1] * len(data)

    final_vec = []
    for i, x in enumerate(lengths):
        final_vec.extend([level_vec[i]] * x)

    return final_vec
