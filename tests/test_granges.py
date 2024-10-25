import pytest

from rds2py import read_rds

from genomicranges import GenomicRanges, GenomicRangesList
import numpy as np

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_granges():
    gr = read_rds("tests/data/granges.rds")

    assert isinstance(gr, GenomicRanges)
    assert gr.get_seqnames("list") == [
        "chr1",
        "chr2",
        "chr2",
        "chr2",
        "chr1",
        "chr1",
        "chr3",
        "chr3",
        "chr3",
        "chr3",
    ]
    assert np.allclose(gr.get_start(), range(101, 111))
    assert len(gr.get_mcols().get_column_names()) == 2
    assert gr.get_strand("list") == ["-", "+", "+", "*", "*", "+", "+", "+", "-", "-"]


def test_granges_list():
    gr = read_rds("tests/data/grangeslist.rds")

    assert isinstance(gr, GenomicRangesList)
    assert len(gr) == 5
