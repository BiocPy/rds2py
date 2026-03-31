"""Low-level interface for reading RData files.

This module provides the core functionality for parsing RData (.RData/.rda) files
and converting them into dictionary representations that can be further processed
by higher-level functions.
"""

from typing import Any, Dict

from .lib_rds_parser import RdaObject, RdsReader
from .PyRdsReader import PyRdsParser

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

    def get_object_count(self) -> int:
        """Get the number of objects stored in the RData file.

        Returns:
            Number of objects.
        """
        return self.rda_object.get_object_count()

    def parse(self) -> Dict[str, Dict[str, Any]]:
        """Parse all objects in the RData file.

        Returns:
            A dictionary mapping object names to their parsed representations.
            Each value has the same structure as the output of
            :py:meth:`~rds2py.PyRdsReader.PyRdsParser.parse`.
        """
        try:
            helper = _RdsProcessorHelper()

            result = {}
            names = self.get_object_names()
            for i, name in enumerate(names):
                reader = self.rda_object.get_object_by_index(i)
                key = name if name is not None else f"__unnamed_{i}"
                result[key] = helper._process_object(reader)

            return result
        except Exception as e:
            raise PyRdaParserError(f"Error parsing RData file: {str(e)}")

    def parse_object(self, name: str) -> Dict[str, Any]:
        """Parse a single named object from the RData file.

        Args:
            name:
                Name of the object to parse.

        Returns:
            A dictionary containing the parsed data for the requested object.
        """
        try:
            helper = _RdsProcessorHelper()
            reader = self.rda_object.get_object_by_name(name)
            return helper._process_object(reader)
        except Exception as e:
            raise PyRdaParserError(f"Error parsing object '{name}': {str(e)}")


class _RdsProcessorHelper(PyRdsParser):
    """Helper that reuses PyRdsParser's object processing without requiring a file."""

    def __init__(self):
        self.R_MIN = -2147483648

    def _process_object(self, obj: RdsReader) -> Dict[str, Any]:
        return super()._process_object(obj)
