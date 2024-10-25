import pytest

from rds2py import read_rds

from multiassayexperiment import MultiAssayExperiment

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_sce():
    data = read_rds("tests/data/simple_mae.rds")

    assert data is not None
    assert isinstance(data, MultiAssayExperiment)
    assert len(data.get_experiment_names()) == 2
