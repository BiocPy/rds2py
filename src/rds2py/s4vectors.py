from .parser import get_class

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def parse_rle(x: dict) -> list:
    """Parse an S4Vector RLE class as list

    Args:
        x:
            Object parsed from the `RDS` file.

            Usually the result of :py:func:`~rds2py.parser.read_rds`.

    Returns:
        List of the RLE from the R Object.
    """
    cls = get_class(x)

    if cls != "Rle":
        raise TypeError("'x' does not contain an 'Rle' object.")
