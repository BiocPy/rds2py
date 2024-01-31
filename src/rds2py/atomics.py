from .generics import REGISTRY, save_rds

from biocutils import BooleanList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def load_boolean_objects(robj: dict):
    _keys = list(robj.keys())

    if list(_keys) == 1 and list(_keys) == ["data"]:
        return BooleanList(robj["data"])


REGISTRY["boolean"] = load_boolean_objects


@save_rds
def save_atomics_objects(x: list):
    pass
