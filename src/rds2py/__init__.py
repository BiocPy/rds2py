import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# from .core import *

from .generics import read_rds
from .read_atomic import parse_boolean_vector, parse_double_vector, parse_integer_vector, parse_string_vector
from .read_matrix import parse_dgcmatrix, parse_dgrmatrix, parse_dgtmatrix, parse_ndarray
from .read_frame import parse_data_frame, parse_dframe