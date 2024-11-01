import pytest

from rds2py import read_rds
from hdf5array import Hdf5CompressedSparseMatrix

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

@pytest.mark.skip(reason="delayedarray uses full file paths. this should be run locally.")
def test_read_h5sparse():
    array = read_rds("tests/data/h5sparse.rds")

    assert array is not None
    assert isinstance(array, Hdf5CompressedSparseMatrix)
    assert array.shape == (200, 200)
