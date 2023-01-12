import pytest

from rds2py.core import PyParsedObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_attrs():
    parsed_obj = PyParsedObject("tests/data/atomic_attr.rds")
    robject_obj = parsed_obj.get_robject()
    array = robject_obj.realize_value()
    attr_names = robject_obj.get_attribute_names()
    attr_values = robject_obj.realize_attr_value()

    assert array is not None
    assert len(array) > 0
    assert len(attr_names) is not None
    assert len(attr_values) is not None
