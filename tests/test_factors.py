from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

## With attributes


def test_read_simple_factors():
    data = read_rds("tests/data/simple_factors.rds")

    assert data is not None
    assert len(data) == 4


def test_roundtrip_factors():
    import os
    import tempfile

    from biocutils import Factor

    from rds2py import read_rds, write_rds

    factor = Factor([0, 1, 0], levels=["A", "B"])
    with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
        rds_path = tmp.name

    try:
        write_rds(factor, rds_path)
        result = read_rds(rds_path)
        assert result == ["A", "B", "A"]
    finally:
        if os.path.exists(rds_path):
            os.unlink(rds_path)
