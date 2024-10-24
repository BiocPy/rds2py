import pytest

from rds2py import read_rds
from biocframe import BiocFrame

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_atomic_lists_df():
    frame = read_rds("tests/data/lists_df.rds")

    assert frame is not None
    assert isinstance(frame, BiocFrame)
    assert len(frame) > 0


def test_read_atomic_lists_nested_deep_rownames():
    frame = read_rds("tests/data/lists_df_rownames.rds")

    assert frame is not None
    assert isinstance(frame, BiocFrame)
    assert len(frame) > 0
