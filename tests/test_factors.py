import pytest

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

## With attributes


def test_read_simple_factors():
    data = read_rds("tests/data/simple_factors.rds")

    assert data is not None
    assert len(data) == 4
