import os
import tempfile

import numpy as np
from biocframe import BiocFrame
from genomicranges import GenomicRanges
from iranges import IRanges

from rds2py import read_rds, save_rds, write_rds


def test_save_rds_genomicranges():
    try:
        from iranges import IRanges

        ir = IRanges(start=[1, 2], width=[10, 20])
    except ImportError:
        ir = None
    if ir is None:
        return

    gr = GenomicRanges(seqnames=["chr1", "chr2"], ranges=ir, strand=["+", "-"], mcols=BiocFrame({"score": [1.0, 2.0]}))

    res = save_rds(gr)
    assert isinstance(res, dict)
    assert "seqnames" in res
    assert "ranges" in res
    assert "strand" in res
    assert "mcols" in res


from summarizedexperiment import SummarizedExperiment


def test_save_rds_summarizedexperiment():
    se = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    res = save_rds(se)
    assert isinstance(res, dict)
    assert "assays" in res
    assert "row_data" in res
    assert "column_data" in res


from singlecellexperiment import SingleCellExperiment


def test_save_rds_singlecellexperiment():
    sce = SingleCellExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])}, reduced_dims={"PCA": np.array([[0.1, 0.2], [0.3, 0.4]])}
    )

    res = save_rds(sce)
    assert isinstance(res, dict)
    assert "reduced_dims" in res
    assert "assays" in res


def test_roundtrip_genomicranges():
    gr = GenomicRanges(
        seqnames=["chr1", "chr2"],
        ranges=IRanges(start=[1, 2], width=[10, 20]),
        strand=["+", "-"],
        mcols=BiocFrame({"score": [1.0, 2.0]}),
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(gr, path)
        result = read_rds(path)

        # Complex objects are saved as GenericVectors with names,
        # so they should be read back as dictionaries.
        assert isinstance(result, dict)
        assert "seqnames" in result
        assert "ranges" in result
        assert "strand" in result
        assert "mcols" in result
    finally:
        os.unlink(path)


def test_roundtrip_summarizedexperiment():
    se = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(se, path)
        result = read_rds(path)

        assert isinstance(result, dict)
        assert "assays" in result
        assert "row_data" in result
        assert "column_data" in result
    finally:
        os.unlink(path)
