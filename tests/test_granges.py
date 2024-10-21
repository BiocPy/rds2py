import pytest

from rds2py.granges import as_granges, as_granges_list
from rds2py.parser import read_rds

from genomicranges import GenomicRanges, GenomicRangesList

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_granges():
    robj = read_rds("tests/data/granges.rds")

    gr = as_granges(robj=robj)

    assert isinstance(gr, GenomicRanges)


def test_granges_list():
    robj = read_rds("tests/data/grangeslist.rds")

    gr = as_granges_list(robj=robj)

    assert isinstance(gr, GenomicRangesList)
    assert len(gr) == 5
