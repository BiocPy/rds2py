"""Low-level interface for reading RDS file format.

This module provides the core functionality for parsing RDS files at a binary level and converting them into a
dictionary representation that can be further processed by higher-level functions.
"""

from typing import Any
from warnings import warn

import numpy as np

from .lib_rds_parser import RdsObject, RdsReader


class PyRdsParserError(Exception):
    """Exception raised for errors during RDS parsing."""


class PyRdsParser:
    """Parser for reading RDS files.

    This class provides low-level access to RDS file contents, handling the binary
    format and converting it into Python data structures. It supports various R
    data types and handles special R cases like NA values, integer sequences and
    range functions.

    Attributes:
        R_MIN:
            Minimum integer value in R, used for handling NA values.

        rds_object:
            Internal representation of the RDS file.

        root_object:
            Root object of the parsed RDS file.
    """

    R_MIN: int = -2147483648

    def __init__(self, file_path: str):
        """Initialize the class.

        Args:
            file_path:
                Path to the RDS file to be read.
        """
        try:
            self.rds_object = RdsObject(file_path)
            robject = self.rds_object.get_robject()

            if not isinstance(robject, RdsReader):
                raise TypeError(f"Expected 'RdsReader' object, got {type(robject)}")

            self.root_object = robject
        except Exception as e:
            raise PyRdsParserError(f"Error initializing 'PyRdsParser': {e!s}")

    def parse(self) -> dict[str, Any]:
        """Parse the entire RDS file into a dictionary structure.

        Returns:
            A dictionary containing the parsed data with keys:
            - 'type': The R object type
            - 'data': The actual data (if applicable)
            - 'attributes': R object attributes (if any)
            - 'class_name': The R class name
            - Additional keys depending on the object type

        Raises:
            PyRdsParserError: If there's an error during parsing.
        """
        try:
            return self._process_object(self.root_object)
        except Exception as e:
            raise PyRdsParserError(f"Error parsing RDS object: {e!s}")

    def _process_object(self, obj: RdsReader) -> dict[str, Any]:
        try:
            rtype = obj.get_rtype()
            result: dict[str, Any] = {"type": rtype}

            if rtype == "S4":
                result["package_name"] = obj.get_package_name()
                result["class_name"] = obj.get_class_name()
                result["attributes"] = self._process_attributes(obj)
            elif rtype in ["integer", "boolean", "double"]:
                result["data"] = self._handle_r_special_cases(
                    self._get_numeric_data(obj, rtype), rtype, obj.get_rsize()
                )
                result["attributes"] = self._process_attributes(obj)
                result["class_name"] = f"{rtype}_vector"
            elif rtype == "string":
                result["data"] = obj.get_string_arr()
                result["class_name"] = "string_vector"
            elif rtype == "vector":
                result["data"] = self._process_vector(obj)
                result["attributes"] = self._process_attributes(obj)
                result["class_name"] = "vector"
            elif rtype == "symbol":
                symbol_name = obj.get_symbol_name()
                if symbol_name == "\001NULL\001":
                    result = {"type": "null"}
                else:
                    result["name"] = symbol_name
                    result["class_name"] = "symbol"
            elif rtype == "null":
                pass
            else:
                # raise ValueError
                warn(f"Unsupported R object type: {rtype}", RuntimeWarning)
                result["data"] = None
                result["attributes"] = None
                result["class_name"] = None

            return result
        except Exception as e:
            raise PyRdsParserError(f"Error processing object: {e!s}")

    def _handle_r_special_cases(self, data: np.ndarray, rtype: str, size: int) -> np.ndarray | range:
        """Handle special R data representations."""
        try:
            # Special handling for R integer containing NA
            if rtype == "integer" and size != 2:
                mask = data == self.R_MIN
                if mask.any():
                    float_data = data.astype(np.float64)
                    float_data[mask] = np.nan
                    return float_data

            # Special handling for R integer sequences
            if rtype == "integer" and size == 2 and data[0] == self.R_MIN and data[1] < 0:
                if data[1] == self.R_MIN:
                    return [None, None]
                return range(data[1] * -1)

            return data
        except Exception as e:
            raise PyRdsParserError(f"Error handling R special cases: {e!s}")

    def _get_numeric_data(self, obj: RdsReader, rtype: str) -> np.ndarray:
        try:
            data = obj.get_numeric_data()
            if rtype == "boolean":
                mask = data == self.R_MIN
                if mask.any():
                    res = data.astype(object)
                    res[mask] = None
                    non_na_mask = ~mask
                    res[non_na_mask] = res[non_na_mask].astype(bool)
                    return res
                else:
                    return data.astype(bool)

            return data
        except Exception as e:
            raise PyRdsParserError(f"Error getting numeric data: {e!s}")

    def _process_vector(self, obj: RdsReader) -> list[dict[str, Any]]:
        return [self._process_object(obj.load_vec_element(i)) for i in range(obj.get_rsize())]

    def _process_attributes(self, obj: RdsReader) -> dict[str, dict[str, Any]]:
        try:
            attributes = {}
            for name in obj.get_attribute_names():
                attr_obj = obj.load_attribute_by_name(name)
                attributes[name] = self._process_object(attr_obj)

            return attributes
        except Exception as e:
            raise PyRdsParserError(f"Error processing attributes: {e!s}")

    def get_dimensions(self) -> tuple | None:
        try:
            return self.root_object.get_dimensions()
        except Exception as e:
            raise PyRdsParserError(f"Error getting dimensions: {e!s}")
