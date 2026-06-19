from multiassayexperiment import MultiAssayExperiment

from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_read_sce():
    data = read_rds("tests/data/simple_mae.rds")

    assert data is not None
    assert isinstance(data, MultiAssayExperiment)
    assert len(data.get_experiment_names()) == 2


def test_save_mae():
    import os
    import tempfile

    from rds2py import save_rds, write_rds

    data = read_rds("tests/data/simple_mae.rds")

    res = save_rds(data)
    assert isinstance(res, dict)
    assert "experiments" in res
    assert "col_data" in res

    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        rds_path = tmp.name
    try:
        write_rds(data, rds_path)
        from rds2py.rdsutils import parse_rds

        parsed = parse_rds(rds_path)
        assert parsed["type"] == "vector"
    finally:
        if os.path.exists(rds_path):
            os.unlink(rds_path)
