#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "rds2cpp/rds2cpp.hpp"
#include <memory>

namespace py = pybind11;

class RdsObject {
private:
    std::unique_ptr<const rds2cpp::RObject> ptr;

public:
    RdsObject(const rds2cpp::RObject* p) : ptr(p) {
        if (!ptr) {
            throw std::runtime_error("Null pointer passed to RdsObject");
        }
    }

    std::string get_type() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_type");
        }
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT: return "integer";
            case rds2cpp::SEXPType::REAL: return "double";
            case rds2cpp::SEXPType::STR: return "string";
            case rds2cpp::SEXPType::LGL: return "boolean";
            case rds2cpp::SEXPType::VEC: return "vector";
            case rds2cpp::SEXPType::S4: return "S4";
            case rds2cpp::SEXPType::NIL: return "null";
            default: return "other";
        }
    }

    int get_size() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_size");
        }
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT:
                return static_cast<const rds2cpp::IntegerVector*>(ptr.get())->data.size();
            case rds2cpp::SEXPType::REAL:
                return static_cast<const rds2cpp::DoubleVector*>(ptr.get())->data.size();
            case rds2cpp::SEXPType::STR:
                return static_cast<const rds2cpp::StringVector*>(ptr.get())->data.size();
            case rds2cpp::SEXPType::LGL:
                return static_cast<const rds2cpp::LogicalVector*>(ptr.get())->data.size();
            case rds2cpp::SEXPType::VEC:
                return static_cast<const rds2cpp::GenericVector*>(ptr.get())->data.size();
            default:
                return -1;
        }
    }

    py::array get_numeric_data() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_numeric_data");
        }
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT: {
                auto vec = static_cast<const rds2cpp::IntegerVector*>(ptr.get());
                return py::array_t<int>({vec->data.size()}, {sizeof(int)}, vec->data.data());
            }
            case rds2cpp::SEXPType::REAL: {
                auto vec = static_cast<const rds2cpp::DoubleVector*>(ptr.get());
                return py::array_t<double>({vec->data.size()}, {sizeof(double)}, vec->data.data());
            }
            case rds2cpp::SEXPType::LGL: {
                auto vec = static_cast<const rds2cpp::LogicalVector*>(ptr.get());
                return py::array_t<int>({vec->data.size()}, {sizeof(int)}, vec->data.data());
            }
            default:
                throw std::runtime_error("Cannot get numeric data from non-numeric type");
        }
    }

    std::vector<std::string> get_string_data() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_string_data");
        }
        if (ptr->type() != rds2cpp::SEXPType::STR) {
            throw std::runtime_error("Cannot get string data from non-string type");
        }
        return static_cast<const rds2cpp::StringVector*>(ptr.get())->data;
    }

    std::vector<std::string> get_attribute_names() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_attribute_names");
        }
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT:
                return static_cast<const rds2cpp::IntegerVector*>(ptr.get())->attributes.names;
            case rds2cpp::SEXPType::REAL:
                return static_cast<const rds2cpp::DoubleVector*>(ptr.get())->attributes.names;
            case rds2cpp::SEXPType::LGL:
                return static_cast<const rds2cpp::LogicalVector*>(ptr.get())->attributes.names;
            case rds2cpp::SEXPType::VEC:
                return static_cast<const rds2cpp::GenericVector*>(ptr.get())->attributes.names;
            case rds2cpp::SEXPType::S4:
                return static_cast<const rds2cpp::S4Object*>(ptr.get())->attributes.names;
            default:
                return std::vector<std::string>();
        }
    }

    RdsObject get_attribute(const std::string& name) const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_attribute");
        }
        const auto& names = get_attribute_names();
        auto it = std::find(names.begin(), names.end(), name);
        if (it == names.end()) {
            throw std::runtime_error("Attribute not found: " + name);
        }
        size_t idx = std::distance(names.begin(), it);
        
        const rds2cpp::RObject* attr_ptr = nullptr;
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT:
                attr_ptr = static_cast<const rds2cpp::IntegerVector*>(ptr.get())->attributes.values[idx].get();
                break;
            case rds2cpp::SEXPType::REAL:
                attr_ptr = static_cast<const rds2cpp::DoubleVector*>(ptr.get())->attributes.values[idx].get();
                break;
            case rds2cpp::SEXPType::LGL:
                attr_ptr = static_cast<const rds2cpp::LogicalVector*>(ptr.get())->attributes.values[idx].get();
                break;
            case rds2cpp::SEXPType::VEC:
                attr_ptr = static_cast<const rds2cpp::GenericVector*>(ptr.get())->attributes.values[idx].get();
                break;
            case rds2cpp::SEXPType::S4:
                attr_ptr = static_cast<const rds2cpp::S4Object*>(ptr.get())->attributes.values[idx].get();
                break;
            default:
                throw std::runtime_error("Cannot get attributes from this type");
        }
        return RdsObject(attr_ptr);
    }

    RdsObject get_vector_element(size_t idx) const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_vector_element");
        }
        if (ptr->type() != rds2cpp::SEXPType::VEC) {
            throw std::runtime_error("Cannot get vector element from non-vector type");
        }
        auto vec = static_cast<const rds2cpp::GenericVector*>(ptr.get());
        if (idx >= vec->data.size()) {
            throw std::runtime_error("Index out of bounds");
        }
        return RdsObject(vec->data[idx].get());
    }

    std::string get_class_name() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_class_name");
        }
        if (ptr->type() != rds2cpp::SEXPType::S4) {
            throw std::runtime_error("Cannot get class name from non-S4 type");
        }
        return static_cast<const rds2cpp::S4Object*>(ptr.get())->class_name;
    }

    std::string get_package_name() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_package_name");
        }
        if (ptr->type() != rds2cpp::SEXPType::S4) {
            throw std::runtime_error("Cannot get package name from non-S4 type");
        }
        return static_cast<const rds2cpp::S4Object*>(ptr.get())->package_name;
    }

    std::pair<size_t, size_t> get_dimensions() const {
        if (!ptr) {
            throw std::runtime_error("Null pointer in get_dimensions");
        }
        if (ptr->type() != rds2cpp::SEXPType::INT) {
            throw std::runtime_error("Cannot get dimensions from non-integer type");
        }
        auto vec = static_cast<const rds2cpp::IntegerVector*>(ptr.get());
        if (vec->data.size() != 2) {
            throw std::runtime_error("Dimensions must be length 2");
        }
        return {static_cast<size_t>(vec->data[0]), static_cast<size_t>(vec->data[1])};
    }
};

class RdsParser {
private:
    std::unique_ptr<rds2cpp::Parsed> parsed;

public:
    RdsParser(const std::string& filename) {
        try {
            parsed = std::make_unique<rds2cpp::Parsed>(rds2cpp::parse_rds(filename));
        } catch (const std::exception& e) {
            throw std::runtime_error("Failed to parse RDS file: " + std::string(e.what()));
        }
    }

    RdsObject get_object() const {
        if (!parsed || !parsed->object) {
            throw std::runtime_error("No valid RDS object available");
        }
        return RdsObject(parsed->object.get());
    }
};

PYBIND11_MODULE(rds_parser, m) {
    m.doc() = "Python bindings for rds2cpp library";

    py::register_exception<std::runtime_error>(m, "RdsParserError");

    py::class_<RdsObject>(m, "RdsObject")
        // .def(py::init<const RdsObject&>())
        .def("get_type", &RdsObject::get_type)
        .def("get_size", &RdsObject::get_size)
        .def("get_numeric_data", &RdsObject::get_numeric_data)
        .def("get_string_data", &RdsObject::get_string_data)
        .def("get_attribute_names", &RdsObject::get_attribute_names)
        .def("get_attribute", &RdsObject::get_attribute)
        .def("get_vector_element", &RdsObject::get_vector_element)
        .def("get_class_name", &RdsObject::get_class_name)
        .def("get_package_name", &RdsObject::get_package_name)
        .def("get_dimensions", &RdsObject::get_dimensions);

    py::class_<RdsParser>(m, "RdsParser")
        .def(py::init<const std::string&>())
        .def("get_object", &RdsParser::get_object);
}