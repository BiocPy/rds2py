from .rds_parser import RdsObject, RdsReader
import numpy as np

class PyRdsParser:
    def __init__(self, file_path):
        self.rds_object = RdsObject(file_path)
        robject = self.rds_object.get_robject()
        if not isinstance(robject, RdsReader):
            raise TypeError("Expected PyRdsReader object, got {}".format(type(robject)))
        self.root_object = robject

    def parse(self):
        return self._process_object(self.root_object)

    def _process_object(self, obj):
        rtype = obj.get_rtype()
        result = {"type": rtype}

        if rtype in ["integer", "boolean", "double"]:
            result["data"] = self._get_numeric_data(obj, rtype)
            result["attributes"] = self._process_attributes(obj)
        elif rtype == "string":
            result["data"] = obj.get_string_arr()
        elif rtype == "vector":
            result["data"] = [self._process_object(obj.load_vec_element(i)) for i in range(obj.get_rsize())]
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

    def _get_numeric_data(self, obj, rtype):
        if rtype in ["integer", "boolean"]:
            return np.array(obj.get_int_or_bool_arr())
        elif rtype == "double":
            return np.array(obj.get_double_arr())
        else:
            raise ValueError(f"Unsupported numeric type: {rtype}")

    def _process_attributes(self, obj):
        attributes = {}
        for name in obj.get_attribute_names():
            attr_obj = obj.load_attribute_by_name(name)
            attributes[name] = self._process_object(attr_obj)
        return attributes

    def get_dimensions(self):
        try:
            return self.root_object.get_dimensions()
        except RuntimeError:
            return None