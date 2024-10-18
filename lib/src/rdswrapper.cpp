#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "rds2cpp/rds2cpp.hpp"
#include <iostream>

namespace py = pybind11;

// Interface methods to Parser Object

inline uintptr_t py_parser_rds_file(std::string file) {
    rds2cpp::Parsed res = rds2cpp::parse_rds(file);

    return reinterpret_cast<uintptr_t>(new rds2cpp::Parsed(std::move(res)));
}

inline uintptr_t py_parser_extract_robject(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::Parsed *>(ptr);
    return reinterpret_cast<uintptr_t>(parsed->object.get());
}

// probably don't need this, mostly for testing
inline void py_read_parsed_ptr(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::Parsed *>(ptr);
}

// Interface Methods to RObject

inline std::string py_robject_extract_type(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return "integer";
        case rds2cpp::SEXPType::REAL:
            return "double";
        case rds2cpp::SEXPType::STR:
            return "string";
        case rds2cpp::SEXPType::LGL:
            return "boolean";
        case rds2cpp::SEXPType::VEC:
            return "vector";
        case rds2cpp::SEXPType::S4:
            return "S4";
        case rds2cpp::SEXPType::NIL:
            return "null";
        default:
            break;
    }
    return "other";
}

template<class Vector>
int _size_(const rds2cpp::RObject* ptr) {
    auto xptr = static_cast<const Vector*>(ptr);
    return xptr->data.size();
}

inline int py_robject_extract_size(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return _size_<rds2cpp::IntegerVector>(parsed);
        case rds2cpp::SEXPType::REAL:
            return _size_<rds2cpp::DoubleVector>(parsed);
        case rds2cpp::SEXPType::STR:
            return _size_<rds2cpp::StringVector>(parsed);
        case rds2cpp::SEXPType::LGL:
            return _size_<rds2cpp::LogicalVector>(parsed);
        case rds2cpp::SEXPType::VEC:
            return _size_<rds2cpp::GenericVector>(parsed);
        default:
            break;
    }
    return -1;
}

template<class Vector>
uintptr_t _get_vector_ptr(const rds2cpp::RObject* ptr) {
    auto xptr = static_cast<const Vector*>(ptr);
    return reinterpret_cast<uintptr_t>(xptr->data.data());
}

inline uintptr_t parse_robject_int_vector(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return _get_vector_ptr<rds2cpp::IntegerVector>(parsed);
        case rds2cpp::SEXPType::LGL:
            return _get_vector_ptr<rds2cpp::LogicalVector>(parsed);
        case rds2cpp::SEXPType::REAL:
            return _get_vector_ptr<rds2cpp::DoubleVector>(parsed);
        default:
            break;
    }
    throw std::runtime_error("cannot obtain numeric values for non-numeric RObject type");
    return _get_vector_ptr<rds2cpp::IntegerVector>(parsed); // avoid compiler warning.
}

// inline uintptr_t parse_robject_double_vector(uintptr_t ptr) {
//     auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
//     switch (parsed->type()) {
//         case rds2cpp::SEXPType::REAL:
//             return _get_vector_ptr<rds2cpp::DoubleVector>(parsed);
//         default:
//             break;
//     }
//     throw std::runtime_error("cannot obtain numeric values for non-numeric RObject type");
//     return _get_vector_ptr<rds2cpp::DoubleVector>(parsed); // avoid compiler warning.
// }

inline std::vector<std::string> parse_robject_string_vector(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    if (parsed->type() != rds2cpp::SEXPType::STR) {
        throw std::runtime_error("cannot return string values for non-string RObject type");
    }
    auto sptr = static_cast<const rds2cpp::StringVector*>(parsed);

    return sptr->data;
}

template<class Object>
const rds2cpp::Attributes& _get_attr_ptr(const rds2cpp::RObject* ptr) {
    auto aptr = static_cast<const Object*>(ptr);
    return aptr->attributes;
}

inline std::vector<std::string> parse_robject_attribute_names(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return _get_attr_ptr<rds2cpp::IntegerVector>(parsed).names;
            break;
        case rds2cpp::SEXPType::REAL:
            return _get_attr_ptr<rds2cpp::DoubleVector>(parsed).names;
            break;
        case rds2cpp::SEXPType::LGL:
            return _get_attr_ptr<rds2cpp::LogicalVector>(parsed).names;
            break;
        case rds2cpp::SEXPType::VEC:
            return _get_attr_ptr<rds2cpp::GenericVector>(parsed).names;
            break;
        case rds2cpp::SEXPType::S4:
            return _get_attr_ptr<rds2cpp::S4Object>(parsed).names;
            break;
        default:
            break;
    }
    return _get_attr_ptr<rds2cpp::IntegerVector>(parsed).names; // avoid compiler warning.
}

template<class Object>
int _contains_attr_(const rds2cpp::RObject* ptr, const std::string& name) {
    auto aptr = static_cast<const Object*>(ptr);
    const auto& attr_names = aptr->attributes.names;

    for (size_t i = 0; i < attr_names.size(); ++i) {
        if (attr_names[i] == name) {
            return i;
        }
    }

    return -1;
}

inline int parse_robject_find_attribute(uintptr_t ptr, std::string name) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return _contains_attr_<rds2cpp::IntegerVector>(parsed, name);
        case rds2cpp::SEXPType::REAL:
            return _contains_attr_<rds2cpp::DoubleVector>(parsed, name);
        case rds2cpp::SEXPType::LGL:
            return _contains_attr_<rds2cpp::LogicalVector>(parsed, name);
        case rds2cpp::SEXPType::STR:
            return _contains_attr_<rds2cpp::StringVector>(parsed, name);
        case rds2cpp::SEXPType::VEC:
            return _contains_attr_<rds2cpp::GenericVector>(parsed, name);
        case rds2cpp::SEXPType::S4:
            return _contains_attr_<rds2cpp::S4Object>(parsed, name);
        default:
            break;
    }
    return -1;
}

template<class AttrClass>
uintptr_t _load_attr_idx_(const rds2cpp::RObject* ptr, int i) {
    auto aptr = static_cast<const AttrClass*>(ptr);
    if (static_cast<size_t>(i) >= aptr->attributes.values.size()) {
        throw std::runtime_error("requested attribute index " + std::to_string(i) + " is out of range");
    }
    const auto& chosen = aptr->attributes.values[i];
    return reinterpret_cast<uintptr_t>(chosen.get());
}

inline uintptr_t parse_robject_load_attribute_by_index(uintptr_t ptr, int i) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    switch (parsed->type()) {
        case rds2cpp::SEXPType::INT:
            return _load_attr_idx_<rds2cpp::IntegerVector>(parsed, i);
        case rds2cpp::SEXPType::REAL:
            return _load_attr_idx_<rds2cpp::IntegerVector>(parsed, i);
        case rds2cpp::SEXPType::LGL:
            return _load_attr_idx_<rds2cpp::LogicalVector>(parsed, i);
        case rds2cpp::SEXPType::STR:
            return _load_attr_idx_<rds2cpp::StringVector>(parsed, i);
        case rds2cpp::SEXPType::VEC:
            return _load_attr_idx_<rds2cpp::GenericVector>(parsed, i);
        case rds2cpp::SEXPType::S4:
            return _load_attr_idx_<rds2cpp::S4Object>(parsed, i);
        default:
            break;
    }

    throw std::runtime_error("unsupported R object type");
    return _load_attr_idx_<rds2cpp::S4Object>(parsed, i); // avoid compiler warnings.
}

inline uintptr_t parse_robject_load_attribute_by_name(uintptr_t ptr, std::string name) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    int idx = parse_robject_find_attribute(ptr, name);
    if (idx < 0) {
        throw std::runtime_error("no attribute named '" + name + "'");
    }
    return parse_robject_load_attribute_by_index(ptr, idx);
}

inline uintptr_t parse_robject_load_vec_element(uintptr_t ptr, int i) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    if (parsed->type() != rds2cpp::SEXPType::VEC) {
        throw std::runtime_error("cannot return list element for non-list R object");
    }
    auto lptr = static_cast<const rds2cpp::GenericVector*>(parsed);
    return reinterpret_cast<uintptr_t>(lptr->data[i].get());
}

inline std::string parse_robject_class_name(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    if (parsed->type() != rds2cpp::SEXPType::S4) {
        throw std::runtime_error("cannot return class name for non-S4 R object");
    }
    auto sptr = static_cast<const rds2cpp::S4Object*>(parsed);
    return sptr->class_name;
}

inline std::string parse_robject_package_name(uintptr_t ptr) {
    auto parsed = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    if (parsed->type() != rds2cpp::SEXPType::S4) {
        throw std::runtime_error("cannot return class name for non-S4 R object");
    }
    auto sptr = static_cast<const rds2cpp::S4Object*>(parsed);
    return sptr->package_name;
}

inline std::pair<size_t, size_t> parse_robject_dimensions(uintptr_t ptr) {
    auto dimobj = reinterpret_cast<const rds2cpp::RObject *>(ptr);
    if (dimobj->type() != rds2cpp::SEXPType::INT) {
        throw std::runtime_error("expected matrix dimensions to be integer");
    }

    auto dimvec = static_cast<const rds2cpp::IntegerVector*>(dimobj);
    const auto& dims = dimvec->data;
    if (dims.size() != 2) {
        throw std::runtime_error("expected matrix dimensions to be of length 2");
    }
    if (dims[0] < 0 || dims[1] < 0) {
        throw std::runtime_error("expected all matrix dimensions to be non-negative");
    }

    return std::pair<size_t, size_t>(dims[0], dims[1]);
}

// Class definitions

class PyRdsReader {
private:
    const rds2cpp::RObject* ptr;
    std::string rtype;
    int rsize;

public:
    static constexpr int R_MIN = -2147483648;

    PyRdsReader(const rds2cpp::RObject* p) : ptr(p) {
        get_rtype();
        get_rsize();
    }

    std::string get_rtype() {
        if (rtype.empty()) {
            rtype = py_robject_extract_type(reinterpret_cast<uintptr_t>(ptr));
        }
        return rtype;
    }

    int get_rsize() {
        if (rsize == 0) {
            rsize = py_robject_extract_size(reinterpret_cast<uintptr_t>(ptr));
        }
        return rsize;
    }

    py::object realize_value() {
        py::dict result;
        result["rtype"] = rtype;

        if (rtype == "integer" || rtype == "boolean") {
            result["data"] = _get_int_or_bool_arr();
            result["attributes"] = realize_attr_value();
        } else if (rtype == "double") {
            result["data"] = _get_double_arr();
            result["attributes"] = realize_attr_value();
        } else if (rtype == "string") {
            result["data"] = _get_string_arr();
        } else if (rtype == "vector") {
            result["data"] = _get_vector_arr();
            result["attributes"] = realize_attr_value();
        } else if (rtype == "null") {
            return result;
        } else if (rtype == "S4") {
            result["package_name"] = get_package_name();
            result["class_name"] = get_class_name();
            result["attributes"] = realize_attr_value();
            return result;
        } else {
            throw std::runtime_error("Cannot realize object of type: " + rtype);
        }

        return shennanigans_to_py_reprs(result);
    }

    py::object shennanigans_to_py_reprs(py::dict result) {
        if (rtype == "integer") {
            py::array_t<int> data = result["data"].cast<py::array_t<int>>();
            if (rsize == 2 && data.at(0) == R_MIN && data.at(1) < 0) {
                // Create a Python range object manually
                py::object range_func = py::module::import("builtins").attr("range");
                result["data"] = range_func(data.at(1) * -1);
            }
        }
        return result;
    }

    py::array _get_int_or_bool_arr() {
        if (rsize == 0) {
            return py::array_t<int>();
        }
        uintptr_t arr_ptr = parse_robject_int_vector(reinterpret_cast<uintptr_t>(ptr));
        return py::array_t<int>({rsize}, {sizeof(int)}, reinterpret_cast<int*>(arr_ptr));
    }

    py::array _get_double_arr() {
        if (rsize == 0) {
            return py::array_t<double>();
        }
        uintptr_t arr_ptr = parse_robject_int_vector(reinterpret_cast<uintptr_t>(ptr));
        return py::array_t<double>({rsize}, {sizeof(double)}, reinterpret_cast<double*>(arr_ptr));
    }

    py::list _get_string_arr() {
        std::vector<std::string> arr_str = parse_robject_string_vector(reinterpret_cast<uintptr_t>(ptr));
        return py::cast(arr_str);
    }

    py::list _get_vector_arr() {
        py::list vec;
        for (int i = 0; i < rsize; ++i) {
            uintptr_t elem_ptr = parse_robject_load_vec_element(reinterpret_cast<uintptr_t>(ptr), i);
            PyRdsReader elem_reader(reinterpret_cast<const rds2cpp::RObject*>(elem_ptr));
            vec.append(elem_reader.realize_value());
        }
        return vec;
    }

    py::list get_attribute_names() {
        return py::cast(parse_robject_attribute_names(reinterpret_cast<uintptr_t>(ptr)));
    }

    int find_attribute(const std::string& name) {
        return parse_robject_find_attribute(reinterpret_cast<uintptr_t>(ptr), name);
    }

    PyRdsReader load_attribute_by_index(int index) {
        uintptr_t tmp = parse_robject_load_attribute_by_index(reinterpret_cast<uintptr_t>(ptr), index);
        return PyRdsReader(reinterpret_cast<const rds2cpp::RObject*>(tmp));
    }

    PyRdsReader load_attribute_by_name(const std::string& name) {
        uintptr_t tmp = parse_robject_load_attribute_by_name(reinterpret_cast<uintptr_t>(ptr), name);
        return PyRdsReader(reinterpret_cast<const rds2cpp::RObject*>(tmp));
    }

    PyRdsReader load_vec_element(int i) {
        uintptr_t tmp = parse_robject_load_vec_element(reinterpret_cast<uintptr_t>(ptr), i);
        return PyRdsReader(reinterpret_cast<const rds2cpp::RObject*>(tmp));
    }

    std::string get_package_name() {
        if (rtype != "S4") {
            throw std::runtime_error("package name does not exist on non-S4 classes");
        }
        return parse_robject_package_name(reinterpret_cast<uintptr_t>(ptr));
    }

    std::string get_class_name() {
        return parse_robject_class_name(reinterpret_cast<uintptr_t>(ptr));
    }

    std::pair<size_t, size_t> get_dimensions() {
        return parse_robject_dimensions(reinterpret_cast<uintptr_t>(ptr));
    }

    py::dict realize_attr_value() {
        py::dict result;
        for (const auto& ro_attr : get_attribute_names()) {
            PyRdsReader tmp_obj = load_attribute_by_name(ro_attr.cast<std::string>());
            result[ro_attr] = tmp_obj.realize_value();
        }
        return result;
    }
};

class PyRdsObject {
private:
    std::unique_ptr<rds2cpp::Parsed> parsed;

public:
    PyRdsObject(const std::string& file) : parsed(std::make_unique<rds2cpp::Parsed>(rds2cpp::parse_rds(file))) {}

    PyRdsReader get_robject() {
        return PyRdsReader(parsed->object.get());
    }
};

PYBIND11_MODULE(lib_rds, m) {
    py::class_<PyRdsObject>(m, "PyRdsObject")
        .def(py::init<const std::string&>())
        .def("get_robject", &PyRdsObject::get_robject);

    py::class_<PyRdsReader>(m, "PyRdsReader")
        .def(py::init<const rds2cpp::RObject*>())
        .def("get_rtype", &PyRdsReader::get_rtype)
        .def("get_rsize", &PyRdsReader::get_rsize)
        .def("realize_value", &PyRdsReader::realize_value)
        .def("get_attribute_names", &PyRdsReader::get_attribute_names)
        .def("find_attribute", &PyRdsReader::find_attribute)
        .def("load_attribute_by_index", &PyRdsReader::load_attribute_by_index)
        .def("load_attribute_by_name", &PyRdsReader::load_attribute_by_name)
        .def("load_vec_element", &PyRdsReader::load_vec_element)
        .def("get_package_name", &PyRdsReader::get_package_name)
        .def("get_class_name", &PyRdsReader::get_class_name)
        .def("get_dimensions", &PyRdsReader::get_dimensions)
        .def("realize_attr_value", &PyRdsReader::realize_attr_value);
}