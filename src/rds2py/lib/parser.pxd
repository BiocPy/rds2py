# pretty basic Cython wrapper

from libcpp.string cimport string as string_c
from libc.stdint cimport uintptr_t
from libcpp.vector cimport vector
from libcpp.utility cimport pair

cdef extern from "rds2cpp_wrapper.cpp":
    uintptr_t py_parser_rds_file(string_c file) except + nogil
    uintptr_t py_parser_extract_robject(int ptr) except + nogil

    void py_read_parsed_ptr(uintptr_t ptr) except + nogil

    string_c py_robject_extract_type(uintptr_t ptr) except + nogil
    int py_robject_extract_size(uintptr_t ptr) except + nogil

    uintptr_t parse_robject_int_vector(uintptr_t ptr) except + nogil
    vector[string_c] parse_robject_string_vector(uintptr_t ptr) except + nogil
    vector[string_c] parse_robject_attribute_names(uintptr_t ptr) except + nogil

    int parse_robject_find_attribute(uintptr_t ptr, string_c name) except + nogil
    uintptr_t parse_robject_load_attribute_by_index(uintptr_t ptr, int i) except + nogil
    uintptr_t parse_robject_load_attribute_by_name(uintptr_t ptr, string_c name) except + nogil
    uintptr_t parse_robject_load_vec_element(uintptr_t ptr, int i)except + nogil

    string_c parse_robject_class_name(uintptr_t ptr) except + nogil
    string_c parse_robject_package_name(uintptr_t ptr) except + nogil

    pair[int, int] parse_robject_dimensions(uintptr_t ptr) except + nogil
