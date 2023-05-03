# pretty basic Cython wrapper

from libcpp.string cimport string as string_c
from libc.stdint cimport uintptr_t
from libcpp.vector cimport vector
from libcpp.utility cimport pair

cdef extern from "rds_parser.cpp":
    uintptr_t py_parser_rds_file(string_c file) nogil except +
    uintptr_t py_parser_extract_robject(int ptr) nogil except +

    void py_read_parsed_ptr(uintptr_t ptr) nogil except +

    string_c py_robject_extract_type(uintptr_t ptr) nogil except +
    int py_robject_extract_size(uintptr_t ptr) nogil except +

    uintptr_t parse_robject_int_vector(uintptr_t ptr) nogil except +
    vector[string_c] parse_robject_string_vector(uintptr_t ptr) nogil except +
    vector[string_c] parse_robject_attribute_names(uintptr_t ptr) nogil except +
    
    int parse_robject_find_attribute(uintptr_t ptr, string_c name) nogil except +
    uintptr_t parse_robject_load_attribute_by_index(uintptr_t ptr, int i) nogil except +
    uintptr_t parse_robject_load_attribute_by_name(uintptr_t ptr, string_c name) nogil except +
    uintptr_t parse_robject_load_vec_element(uintptr_t ptr, int i) except +

    string_c parse_robject_class_name(uintptr_t ptr) nogil except +
    string_c parse_robject_package_name(uintptr_t ptr) nogil except +

    pair[int, int] parse_robject_dimensions(uintptr_t ptr) nogil except +
