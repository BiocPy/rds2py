import pytest

from rds2py import read_rds

from summarizedexperiment import SummarizedExperiment, RangedSummarizedExperiment

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_summ_expt():
    data = read_rds("tests/data/sumexpt.rds")

    assert data is not None
    assert isinstance(data, SummarizedExperiment)
    assert data.shape == (200, 6)


def test_read_ranged_summ_expt():
    data = read_rds("tests/data/ranged_se.rds")

    assert data is not None
    assert isinstance(data, RangedSummarizedExperiment)
    assert data.shape == (200, 6)
