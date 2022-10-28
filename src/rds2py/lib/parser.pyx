# pretty basic Cython wrapper

from parser cimport (
    py_parser_rds_file, py_parser_extract_robject,
    py_robject_extract_type, py_robject_extract_size,
    parse_robject_int_vector,
    parse_robject_string_vector,
    parse_robject_attribute_names,
    parse_robject_find_attribute,
    parse_robject_load_attribute_by_index,
    parse_robject_load_attribute_by_name,
    parse_robject_load_vec_element,
    parse_robject_class_name,
    parse_robject_package_name,
    parse_robject_dimensions
)
from libc.stdint cimport uintptr_t
from libcpp.string cimport string as string_c
from libcpp.vector cimport vector
from cython cimport view

cimport numpy as np
import numpy as np

cdef class PyParsedObject:
    cdef uintptr_t ptr

    def __cinit__(self, file):
        self.ptr = py_parser_rds_file(file.encode())

    def get_robject(self):
        cdef uintptr_t tmp = py_parser_extract_robject(self.ptr)
        return PyRObject(tmp)

cdef _map_ptr_to_view(uintptr_t ptr, shape, itemsize, format_type):
    cdef view.array my_array = view.array(shape=shape, itemsize=itemsize, format=format_type)
    my_array.data = <char *> ptr
    return np.asarray(my_array)

cdef class PyRObject:
    cdef uintptr_t ptr
    cdef string_c rtype
    cdef int rsize
    R_MIN = -2147483648

    def __cinit__(self, p:uintptr_t):
        self.ptr =  p
        self.get_rtype()
        self.get_rsize()

    def get_rtype(self):
        if not hasattr(self, "rtype"):
            self.rtype = py_robject_extract_type(self.ptr)
        return self.rtype

    def get_rsize(self):
        if not hasattr(self, "rsize"):
            self.rsize = py_robject_extract_size(self.ptr)
        return self.rsize

    def shennanigans_to_py_reprs(self, result):
        if result is None:
            return result

        if self.rtype.decode() in ["integer"]:
            if self.rsize == 2 and result["data"][0] == self.R_MIN and result["data"][1] < 0:
                result["data"] = range(result["data"][1] * -1)

        return result

    def realize_value(self):
        result = {}
        if self.rtype.decode() in ["integer", "boolean"]:
            result["data"] = self._get_int_or_bool_arr()
            result["attributes"] = self.realize_attr_value()
        elif self.rtype.decode('UTF-8') in ["double"]:
            result["data"] =  self._get_double_arr()
            result["attributes"] = self.realize_attr_value()
        elif self.rtype.decode('UTF-8') in ["string"]:
            result["data"] =  [s.decode() for s in self._get_string_arr()]
        elif self.rtype.decode('UTF-8') in ["vector"]:
            result["data"] =  self._get_vector_arr()
            result["attributes"] = self.realize_attr_value()
        elif self.rtype.decode('UTF-8') in ["null"]:
            return  None
        elif self.rtype.decode('UTF-8') in ["S4"]:
            result = {
                "data": None,
                "package_name": self.get_package_name(),
                "class_name": self.get_class_name()
            }
            result["attributes"] = self.realize_attr_value()
        else:
            return {
                "data": None,
                "attributes": None
            }
            # raise Exception(f'Cannot realize {self.rtype.decode()}')

        return self.shennanigans_to_py_reprs(result)

    def _get_vector_arr(self):
        vec = []
        for i in range(self.rsize):
            v_obj = self.load_vec_element(i)
            v_obj_val = v_obj.realize_value()
            vec.append(v_obj_val)

        return vec

    def _get_int_or_bool_arr(self):
        if self.rsize == 0:
            return np.empty(shape=(self.rsize,), dtype=int)
        cdef uintptr_t arr_ptr = parse_robject_int_vector(self.ptr)
        return _map_ptr_to_view(arr_ptr, shape=(self.rsize,), itemsize=sizeof(int), format_type="i")

    def _get_double_arr(self):
        if self.rsize == 0:
            return np.empty(shape=(self.rsize,), dtype="f8")
        cdef uintptr_t arr_ptr = parse_robject_int_vector(self.ptr)
        return _map_ptr_to_view(arr_ptr, shape=(self.rsize,), itemsize=sizeof(double), format_type="d")

    def _get_string_arr(self):
        cdef vector[string_c] arr_str = parse_robject_string_vector(self.ptr)
        return arr_str

    def get_attribute_names(self):
        cdef vector[string_c] arr_str = parse_robject_attribute_names(self.ptr)
        return arr_str

    def find_attribute(self, name):
        return parse_robject_find_attribute(self.ptr, name.encode())

    def load_attribute_by_index(self, index):
        cdef uintptr_t tmp =  parse_robject_load_attribute_by_index(self.ptr, index)
        return PyRObject(tmp)

    def load_attribute_by_name(self, name):
        cdef uintptr_t tmp =  parse_robject_load_attribute_by_name(self.ptr, name.encode())
        return PyRObject(tmp)

    def load_vec_element(self, i):
        cdef uintptr_t tmp =  parse_robject_load_vec_element(self.ptr, i)
        return PyRObject(tmp)

    def get_package_name(self):
        if self.rtype.decode() == "S4":
            return parse_robject_package_name(self.ptr).decode()

        raise Exception(f'package name does not exist on non-S4 classes')

    def get_class_name(self):
        if self.rtype.decode() == "S4":
            return parse_robject_class_name(self.ptr).decode()

        raise Exception(f'class name does not exist on non-S4 classes')

    def get_dimensions(self):
        return parse_robject_dimensions(self.ptr)

    def realize_attr_value(self):
        result = {}

        for ro_attr in self.get_attribute_names():
            tmp_obj = self.load_attribute_by_name(ro_attr.decode())
            result[ro_attr.decode()] = tmp_obj.realize_value()

        return result
