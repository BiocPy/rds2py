from .generics import _dispatcher
from .rdsutils import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_vector(robject: dict):
    print("in parse vector")
    _cls = get_class(robject)

    if _cls not in ["vector"]:
        raise RuntimeError(
            f"`robject` does not contain not a vector/dictionary object, contains `{_cls}`."
        )

    if "names" not in robject["attributes"]:
        return [_dispatcher(x) for x in robject["data"]]

    dict_keys = list(_dispatcher(robject["attributes"]["names"]))

    print(dict_keys)
    print("final_vec")
    final_vec = {}
    for idx, dkey in enumerate(dict_keys):
        final_vec[dkey] = _dispatcher(robject["data"][idx])

    return final_vec
