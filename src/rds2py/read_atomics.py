from .rds_interface import load_rds
from .generics import load_rds, save_object

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def load_atomic_objects(robj: dict):
    _keys = list(robj.keys())

    if list(_keys) == 1 and list(_keys) == ["data"]:
        return robj["data"]


@save_object
def save_atomics_objects(x: list):
