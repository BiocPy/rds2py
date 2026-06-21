from singlecellexperiment import SingleCellExperiment

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_sce():
    data = read_rds("tests/data/simple_sce.rds")

    assert data is not None
    assert isinstance(data, SingleCellExperiment)
    assert data.shape == (100, 100)


def test_read_sce_errors():
    import pytest

    from rds2py.read_sce import read_alts_summarized_experiment_by_column, read_single_cell_experiment

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(RuntimeError):
        read_single_cell_experiment(bad_obj)

    with pytest.raises(RuntimeError):
        read_alts_summarized_experiment_by_column(bad_obj)


def test_roundtrip_sce_complex():
    import os
    import tempfile

    import numpy as np
    from singlecellexperiment import SingleCellExperiment

    from rds2py import write_rds

    alt_sce = SingleCellExperiment(assays={"counts": np.array([[10, 20]], dtype=np.int32)})
    sce = SingleCellExperiment(
        assays={"counts": np.array([[1, 2], [3, 4]], dtype=np.int32)},
        reduced_dims={"PCA": np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float64)},
        alternative_experiments={"alt": alt_sce},
    )

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name

    try:
        write_rds(sce, path)
        recreated = read_rds(path)
        assert isinstance(recreated, SingleCellExperiment)
        assert "counts" in recreated.assays
        assert "PCA" in recreated.reduced_dims
        assert np.allclose(recreated.reduced_dims["PCA"], sce.reduced_dims["PCA"])
        assert "alt" in recreated.alternative_experiments
        assert isinstance(recreated.alternative_experiments["alt"], SingleCellExperiment)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_sce_empty_assays():
    import os
    import tempfile

    from singlecellexperiment import SingleCellExperiment

    from rds2py import write_rds

    sce = SingleCellExperiment()
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        path = tmp.name

    try:
        write_rds(sce, path)
        recreated = read_rds(path)
        assert isinstance(recreated, SingleCellExperiment)
        assert len(recreated.assays) == 0
    finally:
        if os.path.exists(path):
            os.unlink(path)
