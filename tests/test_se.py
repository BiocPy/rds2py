from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

from rds2py import read_rds

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


def test_read_se_errors():
    import pytest

    from rds2py.read_se import read_summarized_experiment

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(RuntimeError):
        read_summarized_experiment(bad_obj)


def test_se_empty_assays_and_fallback():
    import os
    import tempfile

    import numpy as np
    from genomicranges import GenomicRanges
    from iranges import IRanges
    from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

    from rds2py import write_rds

    se = SummarizedExperiment()
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name

    try:
        write_rds(se, path)
        recreated = read_rds(path)
        assert isinstance(recreated, SummarizedExperiment)
        assert len(recreated.assays) == 0
    finally:
        if os.path.exists(path):
            os.unlink(path)

    # Test _get fallback/hasattr checks in save_se.py by adding get_metadata dynamically
    se_with_assays = SummarizedExperiment(assays={"counts": np.ones((2, 2))})
    se_with_assays.get_metadata = lambda: se_with_assays.metadata

    try:
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
            path = tmp.name
        try:
            write_rds(se_with_assays, path)
            recreated = read_rds(path)
            assert isinstance(recreated, SummarizedExperiment)
        finally:
            if os.path.exists(path):
                os.unlink(path)
    finally:
        del se_with_assays.get_metadata

    rse = RangedSummarizedExperiment(
        assays={"counts": np.ones((2, 2))},
        row_ranges=GenomicRanges(seqnames=["chr1", "chr2"], ranges=IRanges(start=[1, 2], width=[10, 20])),
    )
    rse.get_metadata = lambda: rse.metadata

    try:
        with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
            path = tmp.name
        try:
            write_rds(rse, path)
            recreated = read_rds(path)
            assert isinstance(recreated, RangedSummarizedExperiment)
        finally:
            if os.path.exists(path):
                os.unlink(path)
    finally:
        del rse.get_metadata
