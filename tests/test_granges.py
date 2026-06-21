import numpy as np
from genomicranges import CompressedGenomicRangesList, GenomicRanges

from rds2py import read_rds

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

    assert isinstance(gr, CompressedGenomicRangesList)
    assert len(gr) == 5


def test_read_granges_errors():
    import pytest

    from rds2py.read_granges import read_genomic_ranges, read_granges_list

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(TypeError):
        read_genomic_ranges(bad_obj)

    with pytest.raises(TypeError):
        read_granges_list(bad_obj)


def test_save_seqinfo_directly():
    import os
    import tempfile

    from genomicranges import SeqInfo

    from rds2py import write_rds

    si = SeqInfo(seqnames=["chrA"], seqlengths=[100], is_circular=[False], genome=["hg38"])

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name
    try:
        write_rds(si, path)
        parsed = read_rds(path)
        assert parsed is not None
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_granges_list_roundtrip_and_fallbacks():
    import os
    import tempfile

    from genomicranges import CompressedGenomicRangesList, GenomicRanges, SeqInfo

    from rds2py import read_rds, save_rds, write_rds

    gr_list = read_rds("tests/data/grangeslist.rds")

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name
    try:
        write_rds(gr_list, path)
        recreated = read_rds(path)
        assert isinstance(recreated, CompressedGenomicRangesList)
        assert len(recreated) == len(gr_list)
    finally:
        if os.path.exists(path):
            os.unlink(path)

    from compressed_lists.base import CompressedList

    orig_get_names = CompressedList.get_names
    try:
        del CompressedList.get_names
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
            path = tmp.name

        try:
            write_rds(gr_list, path)
            recreated = read_rds(path)
            assert isinstance(recreated, CompressedGenomicRangesList)
        finally:
            if os.path.exists(path):
                os.unlink(path)
    finally:
        CompressedList.get_names = orig_get_names
