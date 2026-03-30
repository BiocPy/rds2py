"""Low-level interface for reading RData files.

This module provides the core functionality for parsing RData (.RData/.rda) files
and converting them into dictionary representations that can be further processed
by higher-level functions.
"""

from .lib_rds_parser import RdaObject

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class PyRdaParserError(Exception):
    """Exception raised for errors during RData parsing."""

    pass


class PyRdaParser:
    """Parser for reading RData files.

    This class provides low-level access to RData file contents, handling the binary
    format and converting it into Python data structures. It reuses the same
    ``RdsReader``-based object processing from :py:class:`~.PyRdsParser`.

    Attributes:
        rda_object:
            Internal representation of the RData file.
    """

    def __init__(self, file_path: str):
        """Initialize the parser.

        Args:
            file_path:
                Path to the RData file to be read.
        """
        try:
            self.rda_object = RdaObject(file_path)
        except Exception as e:
            raise PyRdaParserError(f"Error initializing 'PyRdaParser': {str(e)}")

    def get_object_names(self):
        """Get the names of all objects stored in the RData file.

        Returns:
            A list of object names (strings).
        """
        return list(self.rda_object.get_object_names())
