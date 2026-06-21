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


def test_read_factor_errors():
    import pytest
    from rds2py.read_factor import read_factor

    bad_obj = {"type": "S4", "class_name": "BadClass", "attributes": {}}

    with pytest.raises(RuntimeError):
        read_factor(bad_obj)


def test_read_factor_lengths_and_no_levels():
    import pytest
    from rds2py.read_factor import read_factor

    mock_factor_lengths = {
        "type": "integer",
        "class_name": "factor",
        "data": [1, 2],
        "attributes": {
            "levels": {"type": "string", "data": ["A", "B"], "class_name": "string_vector"},
            "lengths": {"type": "integer", "data": [2, 3], "class_name": "integer_vector"},
        },
    }
    res = read_factor(mock_factor_lengths)
    assert res == ["A", "A", "B", "B", "B"]

    mock_factor_no_levels = {"type": "integer", "class_name": "factor", "data": [1, 2], "attributes": {}}
    with pytest.raises(TypeError):
        read_factor(mock_factor_no_levels)
