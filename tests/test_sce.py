import pytest

from rds2py import read_rds

from singlecellexperiment import SingleCellExperiment

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_sce():
    data = read_rds("tests/data/simple_sce.rds")

    assert data is not None
    assert isinstance(data, SingleCellExperiment)
    assert data.shape == (100, 100)
