from .generics import _dispatcher

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_factor(robject: dict):
    print("in parsing factors")
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
