from rds2py import read_rds

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

## With attributes


def test_read_simple_rle():
    data = read_rds("tests/data/simple_rle.rds")

    assert data is not None
    assert len(data) == 36


def test_rle_errors_and_edge_cases():
    import pytest

    from rds2py.read_rle import read_rle

    with pytest.raises(RuntimeError):
        read_rle({"type": "S4", "class_name": "BadClass"})

    mock_rle = {
        "type": "S4",
        "class_name": "Rle",
        "attributes": {"values": {"type": "integer", "data": [1, 2], "class_name": "integer_vector"}},
    }
    res = read_rle(mock_rle)
    assert res == [1, 2]
