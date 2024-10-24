from typing import Any, Dict, List, Union
from warnings import warn

import numpy as np

from .rds_parser import RdsObject, RdsReader


class PyRdsParserError(Exception):
    pass


class PyRdsParser:
    """Python bindings to the rds2cpp interface."""

    R_MIN: int = -2147483648

    def __init__(self, file_path: str):
        try:
            self.rds_object = RdsObject(file_path)
            robject = self.rds_object.get_robject()
            if not isinstance(robject, RdsReader):
                raise TypeError(f"Expected 'RdsReader' object, got {type(robject)}")
            self.root_object = robject
        except Exception as e:
            raise PyRdsParserError(f"Error initializing 'PyRdsParser': {str(e)}")

    def parse(self) -> Dict[str, Any]:
        """Parse the RDS File (recursively).

        Returns:
            A Dictionary with object attributes as keys and the value representing the data from the RDS file.
        """
        try:
            return self._process_object(self.root_object)
        except Exception as e:
            raise PyRdsParserError(f"Error parsing RDS object: {str(e)}")

    def _process_object(self, obj: RdsReader) -> Dict[str, Any]:
        try:
            rtype = obj.get_rtype()
            result: Dict[str, Any] = {"type": rtype}

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
            raise PyRdsParserError(f"Error processing object: {str(e)}")

    def _handle_r_special_cases(
        self, data: np.ndarray, rtype: str, size: int
    ) -> Union[np.ndarray, range]:
        """Handle special R data representations."""
        try:
            # Special handling for R integer containing NA
            if size != 2:
                if any(data == self.R_MIN):
                    return [None if x == self.R_MIN else x for x in data]

            # Special handling for R integer sequences
            if (
                rtype == "integer"
                and size == 2
                and data[0] == self.R_MIN
                and data[1] < 0
            ):
                if data[1] == self.R_MIN:
                    return [None, None]
                return range(data[1] * -1)

            return data
        except Exception as e:
            raise PyRdsParserError(f"Error handling R special cases: {str(e)}")

    def _get_numeric_data(self, obj: RdsReader, rtype: str) -> np.ndarray:
        try:
            data = obj.get_numeric_data()
            if rtype == "boolean":
                return data.astype(bool)
            return data
        except Exception as e:
            raise PyRdsParserError(f"Error getting numeric data: {str(e)}")

    def _process_vector(self, obj: RdsReader) -> List[Dict[str, Any]]:
        return [
            self._process_object(obj.load_vec_element(i))
            for i in range(obj.get_rsize())
        ]

    def _process_attributes(self, obj: RdsReader) -> Dict[str, Dict[str, Any]]:
        try:
            attributes = {}
            for name in obj.get_attribute_names():
                attr_obj = obj.load_attribute_by_name(name)
                attributes[name] = self._process_object(attr_obj)
            return attributes
        except Exception as e:
            raise PyRdsParserError(f"Error processing attributes: {str(e)}")

    def get_dimensions(self) -> Union[tuple, None]:
        try:
            return self.root_object.get_dimensions()
        except Exception as e:
            raise PyRdsParserError(f"Error getting dimensions: {str(e)}")
