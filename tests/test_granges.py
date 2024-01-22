import pytest

from rds2py.granges import as_granges
from rds2py.parser import read_rds

from genomicranges import GenomicRanges

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_granges():
    robj = read_rds("tests/data/granges.rds")

    gr = as_granges(robj=robj)

    assert isinstance(gr, GenomicRanges)
