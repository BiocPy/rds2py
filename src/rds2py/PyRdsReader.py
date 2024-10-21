from .rds_parser import RdsObject, RdsReader
import numpy as np
from typing import Dict, Any, List, Union
from warnings import warn


class PyRdsParserError(Exception):
    pass


class PyRdsParser:
    """Python bindings to the rds2cpp interface."""

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

            if rtype in ["integer", "boolean", "double"]:
                result["data"] = self._get_numeric_data(obj, rtype)
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "string":
                result["data"] = obj.get_string_arr()
            elif rtype == "vector":
                result["data"] = self._process_vector(obj)
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "S4":
                result["package_name"] = obj.get_package_name()
                result["class_name"] = obj.get_class_name()
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "null":
                pass
            else:
                # raise ValueError
                warn(f"Unsupported R object type: {rtype}")
                result["data"] = None
                result["attributes"] = None

            return result
        except Exception as e:
            raise PyRdsParserError(f"Error processing object: {str(e)}")

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
