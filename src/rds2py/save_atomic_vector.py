from biocutils import BooleanList, FloatList, IntegerList, StringList

from .generics import save_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@save_rds.register
def save_integer_vector(x: IntegerList, path: str):
    obj = IntegerList(robject["data"], names=_names)
    return obj