from .rds_parser import RdsObject, RdsReader
import numpy as np


class RdsParserError(Exception):
    pass


class PyRdsParser:
    def __init__(self, file_path):
        try:
            self.rds_object = RdsObject(file_path)
            robject = self.rds_object.get_robject()
            if not isinstance(robject, RdsReader):
                raise TypeError(f"Expected RdsReader object, got {type(robject)}")
            self.root_object = robject
        except Exception as e:
            raise RdsParserError(f"Error initializing RdsParser: {str(e)}")

    def parse(self):
        try:
            return self._process_object(self.root_object)
        except Exception as e:
            raise RdsParserError(f"Error parsing RDS object: {str(e)}")

    def _process_object(self, obj):
        try:
            rtype = obj.get_rtype()
            result = {"type": rtype}

            if rtype in ["integer", "boolean", "double"]:
                result["data"] = self._get_numeric_data(obj, rtype)
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "string":
                result["data"] = obj.get_string_arr()
            elif rtype == "vector":
                result["data"] = [
                    self._process_object(obj.load_vec_element(i))
                    for i in range(obj.get_rsize())
                ]
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "S4":
                result["package_name"] = obj.get_package_name()
                result["class_name"] = obj.get_class_name()
                result["attributes"] = self._process_attributes(obj)
            elif rtype == "null":
                pass
            else:
                raise ValueError(f"Unsupported R object type: {rtype}")

            return result
        except Exception as e:
            raise RdsParserError(f"Error processing object: {str(e)}")

    def _get_numeric_data(self, obj, rtype):
        try:
            if rtype in ["integer", "boolean"]:
                return np.array(obj.get_int_or_bool_arr())
            elif rtype == "double":
                return np.array(obj.get_double_arr())
            else:
                raise ValueError(f"Unsupported numeric type: {rtype}")
        except Exception as e:
            raise RdsParserError(f"Error getting numeric data: {str(e)}")

    def _process_attributes(self, obj):
        try:
            attributes = {}
            for name in obj.get_attribute_names():
                attr_obj = obj.load_attribute_by_name(name)
                attributes[name] = self._process_object(attr_obj)
            return attributes
        except Exception as e:
            raise RdsParserError(f"Error processing attributes: {str(e)}")

    def get_dimensions(self):
        try:
            return self.root_object.get_dimensions()
        except Exception as e:
            raise RdsParserError(f"Error getting dimensions: {str(e)}")
