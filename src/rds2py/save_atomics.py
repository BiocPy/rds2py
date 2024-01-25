from .rds_interface import
from .generics import save_object

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_object.register
def save_atomics_objects(x: list, path: str):
