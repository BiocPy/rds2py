import pytest

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_simple_lists():
    obj = read_rds("tests/data/simple_list.rds")

    assert obj is not None
    assert len(obj) > 0

    assert "collab" in obj
    assert len(obj["collab"]) > 0
