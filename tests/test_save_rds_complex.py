import os
import tempfile

import numpy as np
from biocframe import BiocFrame
from genomicranges import GenomicRanges
from iranges import IRanges
from singlecellexperiment import SingleCellExperiment
from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

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
    assert res["type"] == "S4"
    assert res["class_name"] == "GRanges"
    assert "seqnames" in res["attributes"]
    assert "ranges" in res["attributes"]
    assert "strand" in res["attributes"]
    assert "elementMetadata" in res["attributes"]


def test_save_rds_summarizedexperiment():
    se = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    res = save_rds(se)
    assert isinstance(res, dict)
    assert res["type"] == "S4"
    assert res["class_name"] == "SummarizedExperiment"
    assert "assays" in res["attributes"]
    assert "elementMetadata" in res["attributes"]
    assert "colData" in res["attributes"]


def test_save_rds_singlecellexperiment():
    sce = SingleCellExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])}, reduced_dims={"PCA": np.array([[0.1, 0.2], [0.3, 0.4]])}
    )

    res = save_rds(sce)
    assert isinstance(res, dict)
    assert res["type"] == "S4"
    assert res["class_name"] == "SingleCellExperiment"
    assert "assays" in res["attributes"]
    assert "int_colData" in res["attributes"]


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

        assert isinstance(result, GenomicRanges)
        assert list(result.seqnames) == ["chr1", "chr2"]
        assert list(result.get_strand()) == [1, -1]
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

        assert isinstance(result, SummarizedExperiment)
        assert "counts" in result.assays
        assert result.shape == (2, 2)
    finally:
        os.unlink(path)


def test_save_rds_rangedsummarizedexperiment():
    from genomicranges import GenomicRanges
    from iranges import IRanges

    rse = RangedSummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_ranges=GenomicRanges(seqnames=["chr1", "chr2"], ranges=IRanges(start=[1, 2], width=[10, 20])),
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    res = save_rds(rse)
    assert isinstance(res, dict)
    assert res["type"] == "S4"
    assert res["class_name"] == "RangedSummarizedExperiment"
    assert "assays" in res["attributes"]
    assert "rowRanges" in res["attributes"]
    assert "colData" in res["attributes"]


def test_write_rds_complex():
    from genomicranges import GenomicRanges
    from iranges import IRanges

    rse = RangedSummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])},
        row_ranges=GenomicRanges(seqnames=["chr1", "chr2"], ranges=IRanges(start=[1, 2], width=[10, 20])),
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    sce = SingleCellExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]])}, reduced_dims={"PCA": np.array([[0.1, 0.2], [0.3, 0.4]])}
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        rse_path = f.name
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        sce_path = f.name

    try:
        write_rds(rse, rse_path)
        write_rds(sce, sce_path)

        from rds2py.rdsutils import parse_rds

        assert parse_rds(rse_path)["type"] == "S4"
        assert parse_rds(sce_path)["type"] == "S4"
    finally:
        if os.path.exists(rse_path):
            os.unlink(rse_path)
        if os.path.exists(sce_path):
            os.unlink(sce_path)
