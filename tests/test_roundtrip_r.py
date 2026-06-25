import os
import shutil
import subprocess
import tempfile

import numpy as np
import pytest
from biocframe import BiocFrame
from biocutils import Factor
from genomicranges import GenomicRanges
from iranges import IRanges
from singlecellexperiment import SingleCellExperiment
from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment

from rds2py import read_rds, write_rds

r_available = shutil.which("Rscript") is not None
pytestmark = pytest.mark.skipif(not r_available, reason="Rscript not found on PATH")


def run_r_script(script_code: str):
    with tempfile.NamedTemporaryFile(suffix=".R", mode="w", delete=False) as f:
        f.write(script_code)
        script_path = f.name
    try:
        res = subprocess.run(["Rscript", script_path], capture_output=True, text=True)
        if res.returncode != 0:
            print("STDOUT:", res.stdout)
            print("STDERR:", res.stderr)
            raise RuntimeError(f"Rscript failed with exit code {res.returncode}")
        return res.stdout
    finally:
        os.unlink(script_path)


def test_roundtrip_r_summarizedexperiment():
    se = SummarizedExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]], dtype=np.int32)},
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(se, path)
        script = f"""
        library(SummarizedExperiment)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "SummarizedExperiment"))
        stopifnot(all(dim(obj) == c(2, 2)))
        stopifnot(assayNames(obj) == "counts")
        stopifnot(all(as.matrix(assay(obj)) == matrix(c(1L, 3L, 2L, 4L), nrow=2)))
        stopifnot(all(colnames(obj) == c("c1", "c2")))
        stopifnot(all(rowData(obj)$gene == c("g1", "g2")))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_rangedsummarizedexperiment():
    rse = RangedSummarizedExperiment(
        assays={"counts": np.array([[10, 20], [30, 40]], dtype=np.int32)},
        row_ranges=GenomicRanges(
            seqnames=["chr1", "chr2"], ranges=IRanges(start=[100, 200], width=[10, 20]), strand=["+", "-"]
        ),
        row_data=BiocFrame({"gene": ["g1", "g2"]}),
        column_data=BiocFrame({"cell": ["c1", "c2"]}),
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(rse, path)
        script = f"""
        library(SummarizedExperiment)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "RangedSummarizedExperiment"))
        stopifnot(all(dim(obj) == c(2, 2)))
        rr <- rowRanges(obj)
        stopifnot(is(rr, "GRanges"))
        stopifnot(all(seqnames(rr) == c("chr1", "chr2")))
        stopifnot(all(start(rr) == c(100, 200)))
        stopifnot(all(width(rr) == c(10, 20)))
        stopifnot(all(as.character(strand(rr)) == c("+", "-")))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_singlecellexperiment():
    sce = SingleCellExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]], dtype=np.int32)},
        reduced_dims={"PCA": np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float64)},
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(sce, path)
        script = f"""
        library(SingleCellExperiment)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "SingleCellExperiment"))
        pca <- reducedDim(obj, "PCA")
        stopifnot(is.matrix(pca))
        stopifnot(all(dim(pca) == c(2, 2)))
        stopifnot(all(pca == matrix(c(0.1, 0.3, 0.2, 0.4), nrow=2)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_genomicranges():
    gr = GenomicRanges(
        seqnames=["chrA", "chrB"],
        ranges=IRanges(start=[10, 20], width=[5, 15]),
        strand=["+", "*"],
        mcols=BiocFrame({"score": [1.5, 2.5]}),
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(gr, path)
        script = f"""
        library(GenomicRanges)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "GRanges"))
        stopifnot(all(seqnames(obj) == c("chrA", "chrB")))
        stopifnot(all(start(obj) == c(10, 20)))
        stopifnot(all(width(obj) == c(5, 15)))
        stopifnot(all(as.character(strand(obj)) == c("+", "*")))
        stopifnot(all(mcols(obj)$score == c(1.5, 2.5)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_iranges():
    ir = IRanges(start=[1, 5, 10], width=[3, 4, 5])

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(ir, path)
        script = f"""
        library(IRanges)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "IRanges"))
        stopifnot(all(start(obj) == c(1, 5, 10)))
        stopifnot(all(width(obj) == c(3, 4, 5)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_multiassayexperiment():
    mae = read_rds("tests/data/simple_mae.rds")

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(mae, path)
        script = f"""
        library(MultiAssayExperiment)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "MultiAssayExperiment"))
        stopifnot(length(experiments(obj)) == 2)
        stopifnot(identical(names(experiments(obj)), c("methyl 2k", "methyl 3k")))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_factor():
    factor = Factor([0, 1, 0], levels=["X", "Y"])

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(factor, path)
        script = f"""
        obj <- readRDS("{path}")
        stopifnot(is.factor(obj))
        stopifnot(all(levels(obj) == c("X", "Y")))
        stopifnot(all(as.integer(obj) == c(1, 2, 1)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_biocframe():
    bf = BiocFrame({"colA": [1, 2, 3], "colB": ["foo", "bar", "baz"]}, row_names=["r1", "r2", "r3"])

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(bf, path)
        script = f"""
        library(S4Vectors)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "DFrame"))
        stopifnot(all(rownames(obj) == c("r1", "r2", "r3")))
        stopifnot(all(obj$colA == c(1, 2, 3)))
        stopifnot(all(obj$colB == c("foo", "bar", "baz")))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_sparse_matrices():
    import scipy.sparse as sp

    # CSC Matrix -> dgCMatrix
    csc = sp.csc_matrix([[1, 0], [0, 2]], dtype=np.float64)
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name
    try:
        write_rds(csc, path)
        script = f"""
        library(Matrix)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "dgCMatrix"))
        stopifnot(all(dim(obj) == c(2, 2)))
        stopifnot(all(as.matrix(obj) == matrix(c(1, 0, 0, 2), nrow=2)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)

    # CSR Matrix -> dgRMatrix
    csr = sp.csr_matrix([[1, 0], [0, 2]], dtype=np.float64)
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name
    try:
        write_rds(csr, path)
        script = f"""
        library(Matrix)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "dgRMatrix"))
        stopifnot(all(dim(obj) == c(2, 2)))
        stopifnot(all(as.matrix(obj) == matrix(c(1, 0, 0, 2), nrow=2)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)

    # COO Matrix -> dgTMatrix
    coo = sp.coo_matrix([[1, 0], [0, 2]], dtype=np.float64)
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name
    try:
        write_rds(coo, path)
        script = f"""
        library(Matrix)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "dgTMatrix"))
        stopifnot(all(dim(obj) == c(2, 2)))
        stopifnot(all(as.matrix(obj) == matrix(c(1, 0, 0, 2), nrow=2)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_roundtrip_r_singlecellexperiment_sparse_assay():
    import scipy.sparse as sp

    # SCE with a sparse matrix assay
    csc = sp.csc_matrix([[1, 0], [0, 2]], dtype=np.float64)
    sce = SingleCellExperiment(
        assays={"counts": csc},
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as f:
        path = f.name

    try:
        write_rds(sce, path)
        script = f"""
        library(SingleCellExperiment)
        obj <- readRDS("{path}")
        stopifnot(is(obj, "SingleCellExperiment"))
        stopifnot(all(dim(obj) == c(2, 2)))
        stopifnot(is(assay(obj), "dgCMatrix"))
        stopifnot(all(as.matrix(assay(obj)) == matrix(c(1, 0, 0, 2), nrow=2)))
        """
        run_r_script(script)
    finally:
        if os.path.exists(path):
            os.unlink(path)
