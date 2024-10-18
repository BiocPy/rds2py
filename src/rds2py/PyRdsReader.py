from typing import Dict, List, Union, Tuple
import numpy as np
from .rds_parser import RdsParser, RdsObject, RdsParserError

class PyRdsValue:
    """Python wrapper for RDS values"""
    def __init__(self, obj: RdsObject):
        self.obj = obj
        try:
            self._type = obj.get_type()
            self._size = obj.get_size()
        except RdsParserError as e:
            raise ValueError(f"Failed to initialize PyRdsValue: {str(e)}")

    def realize_value(self) -> Dict:
        """Convert the RDS object into a Python dictionary representation"""
        try:
            result = {"rtype": self._type}

            if self._type in ["integer", "boolean", "double"]:
                result["data"] = self._get_numeric_data()
                result["attributes"] = self._get_attributes()
                result["class_name"] = f"{self._type}_vector"
            
            elif self._type == "string":
                result["data"] = self.obj.get_string_data()
                result["class_name"] = "string_vector"
            
            elif self._type == "vector":
                result["data"] = self._get_vector_data()
                result["attributes"] = self._get_attributes()
                result["class_name"] = "vector"
            
            elif self._type == "S4":
                result["package_name"] = self.obj.get_package_name()
                result["class_name"] = self.obj.get_class_name()
                result["attributes"] = self._get_attributes()
            
            elif self._type == "null":
                pass
            
            else:
                raise ValueError(f"Unsupported R object type: {self._type}")

            return self._handle_special_cases(result)
        except RdsParserError as e:
            raise ValueError(f"Failed to realize value: {str(e)}")

    def _get_numeric_data(self) -> np.ndarray:
        """Get numeric data from the RDS object"""
        try:
            return self.obj.get_numeric_data()
        except RdsParserError as e:
            raise ValueError(f"Failed to get numeric data: {str(e)}")

    def _get_vector_data(self) -> List:
        """Get vector data from the RDS object"""
        try:
            return [PyRdsValue(self.obj.get_vector_element(i)).realize_value() 
                    for i in range(self._size)]
        except RdsParserError as e:
            raise ValueError(f"Failed to get vector data: {str(e)}")

    def _get_attributes(self) -> Dict:
        """Get attributes from the RDS object"""
        try:
            result = {}
            for name in self.obj.get_attribute_names():
                attr_obj = self.obj.get_attribute(name)
                result[name] = PyRdsValue(attr_obj).realize_value()
            return result
        except RdsParserError as e:
            raise ValueError(f"Failed to get attributes: {str(e)}")

    def _handle_special_cases(self, result: Dict) -> Dict:
        """Handle special cases like R's NA values and ranges"""
        if self._type == "integer" and self._size == 2:
            data = result.get("data")
            if data is not None and len(data) == 2:
                if data[0] == -2147483648 and data[1] < 0:  # R's NA value
                    result["data"] = range(-data[1])
        return result

    def get_dimensions(self) -> Tuple[int, int]:
        """Get dimensions of the RDS object"""
        try:
            return self.obj.get_dimensions()
        except RdsParserError as e:
            raise ValueError(f"Failed to get dimensions: {str(e)}")

class PyRdsReader:
    """Main class for reading RDS files"""
    def __init__(self, filename: str):
        try:
            self.parser = RdsParser(filename)
            self.root_object = self.parser.get_object()
        except RdsParserError as e:
            raise IOError(f"Failed to initialize RDS parser: {str(e)}")

    def read(self) -> Dict:
        """Read and parse the RDS file"""
        try:
            return PyRdsValue(self.root_object).realize_value()
        except ValueError as e:
            raise IOError(f"Failed to read RDS file: {str(e)}")

    def get_type(self) -> str:
        """Get the type of the root RDS object"""
        try:
            return self.root_object.get_type()
        except RdsParserError as e:
            raise ValueError(f"Failed to get root object type: {str(e)}")

    def get_size(self) -> int:
        """Get the size of the root RDS object"""
        try:
            return self.root_object.get_size()
        except RdsParserError as e:
            raise ValueError(f"Failed to get root object size: {str(e)}")

    def get_attribute_names(self) -> List[str]:
        """Get attribute names of the root RDS object"""
        try:
            return self.root_object.get_attribute_names()
        except RdsParserError as e:
            raise ValueError(f"Failed to get root object attribute names: {str(e)}")

    def get_attribute(self, name: str) -> Dict:
        """Get a specific attribute of the root RDS object"""
        try:
            attr_obj = self.root_object.get_attribute(name)
            return PyRdsValue(attr_obj).realize_value()
        except RdsParserError as e:
            raise ValueError(f"Failed to get attribute '{name}': {str(e)}")

    def get_class_name(self) -> str:
        """Get the class name of the root RDS object (for S4 objects)"""
        try:
            return self.root_object.get_class_name()
        except RdsParserError as e:
            raise ValueError(f"Failed to get root object class name: {str(e)}")

    def get_package_name(self) -> str:
        """Get the package name of the root RDS object (for S4 objects)"""
        try:
            return self.root_object.get_package_name()
        except RdsParserError as e:
            raise ValueError(f"Failed to get root object package name: {str(e)}")
