#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "rds2cpp/rds2cpp.hpp"
#include <stdexcept>

namespace py = pybind11;

class RdsReader {
private:
    const rds2cpp::RObject* ptr;

public:
    RdsReader(const rds2cpp::RObject* p) : ptr(p) {
        if (!p) throw std::runtime_error("Null pointer passed to RdsReader");
    }

    std::string get_rtype() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_rtype");
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

    int get_rsize() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_rsize");
        try {
            switch (ptr->type()) {
                case rds2cpp::SEXPType::INT: return static_cast<const rds2cpp::IntegerVector*>(ptr)->data.size();
                case rds2cpp::SEXPType::REAL: return static_cast<const rds2cpp::DoubleVector*>(ptr)->data.size();
                case rds2cpp::SEXPType::STR: return static_cast<const rds2cpp::StringVector*>(ptr)->data.size();
                case rds2cpp::SEXPType::LGL: return static_cast<const rds2cpp::LogicalVector*>(ptr)->data.size();
                case rds2cpp::SEXPType::VEC: return static_cast<const rds2cpp::GenericVector*>(ptr)->data.size();
                default: return -1;
            }
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_rsize: ") + e.what());
        }
    }

    py::object realize_value() const {
        if (!ptr) throw std::runtime_error("Null pointer in realize_value");
        try {
            std::string rtype = get_rtype();
            py::dict result;
            result["rtype"] = rtype;

            if (rtype == "integer" || rtype == "boolean") {
                result["data"] = get_int_or_bool_arr();
                result["attributes"] = realize_attr_value();
                result["class_name"] = rtype + "_vector";
            } else if (rtype == "double") {
                result["data"] = get_double_arr();
                result["attributes"] = realize_attr_value();
                result["class_name"] = "double_vector";
            } else if (rtype == "string") {
                result["data"] = get_string_arr();
                result["class_name"] = "string_vector";
            } else if (rtype == "vector") {
                result["data"] = get_vector_arr();
                result["attributes"] = realize_attr_value();
                result["class_name"] = "vector";
            } else if (rtype == "S4") {
                result["package_name"] = get_package_name();
                result["class_name"] = get_class_name();
                result["attributes"] = realize_attr_value();
            } else if (rtype == "null") {
                return result;
            } else {
                throw std::runtime_error("Cannot realize object of type: " + rtype);
            }

            return result;
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in realize_value: ") + e.what());
        }
    }

    py::array get_int_or_bool_arr() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_int_or_bool_arr");
        try {
            if (ptr->type() == rds2cpp::SEXPType::INT) {
                const auto& data = static_cast<const rds2cpp::IntegerVector*>(ptr)->data;
                return py::array_t<int32_t>(data.size(), data.data());
            } else if (ptr->type() == rds2cpp::SEXPType::LGL) {
                const auto& data = static_cast<const rds2cpp::LogicalVector*>(ptr)->data;
                return py::array_t<int32_t>(data.size(), data.data());
            }
            throw std::runtime_error("Invalid type for int_or_bool_arr");
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_int_or_bool_arr: ") + e.what());
        }
    }

    py::array get_double_arr() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_double_arr");
        try {
            if (ptr->type() == rds2cpp::SEXPType::REAL) {
                const auto& data = static_cast<const rds2cpp::DoubleVector*>(ptr)->data;
                return py::array_t<double>(data.size(), data.data());
            }
            throw std::runtime_error("Invalid type for double_arr");
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_double_arr: ") + e.what());
        }
    }

    py::list get_string_arr() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_string_arr");
        try {
            if (ptr->type() == rds2cpp::SEXPType::STR) {
                const auto& data = static_cast<const rds2cpp::StringVector*>(ptr)->data;
                py::list result;
                for (const auto& s : data) {
                    result.append(s);
                }
                return result;
            }
            throw std::runtime_error("Invalid type for string_arr");
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_string_arr: ") + e.what());
        }
    }

    py::list get_vector_arr() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_vector_arr");
        try {
            if (ptr->type() == rds2cpp::SEXPType::VEC) {
                const auto& data = static_cast<const rds2cpp::GenericVector*>(ptr)->data;
                py::list result;
                for (const auto& elem : data) {
                    result.append(RdsReader(elem.get()).realize_value());
                }
                return result;
            }
            throw std::runtime_error("Invalid type for vector_arr");
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_vector_arr: ") + e.what());
        }
    }

    py::dict realize_attr_value() const {
        if (!ptr) throw std::runtime_error("Null pointer in realize_attr_value");
        try {
            py::dict result;
            const auto& attributes = get_attributes();
            for (size_t i = 0; i < attributes.names.size(); ++i) {
                result[py::str(attributes.names[i])] = RdsReader(attributes.values[i].get()).realize_value();
            }
            return result;
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in realize_attr_value: ") + e.what());
        }
    }

    py::list get_attribute_names() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_attribute_names");
        try {
            const auto& attributes = get_attributes();
            return py::cast(attributes.names);
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_attribute_names: ") + e.what());
        }
    }

    int find_attribute(const std::string& name) const {
        if (!ptr) throw std::runtime_error("Null pointer in find_attribute");
        try {
            const auto& attributes = get_attributes();
            auto it = std::find(attributes.names.begin(), attributes.names.end(), name);
            return it != attributes.names.end() ? std::distance(attributes.names.begin(), it) : -1;
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in find_attribute: ") + e.what());
        }
    }

    py::object load_attribute_by_index(int index) const {
        if (!ptr) throw std::runtime_error("Null pointer in load_attribute_by_index");
        try {
            const auto& attributes = get_attributes();
            if (index < 0 || static_cast<size_t>(index) >= attributes.values.size()) {
                throw std::out_of_range("Attribute index out of range");
            }
            return py::cast(new RdsReader(attributes.values[index].get()));
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in load_attribute_by_index: ") + e.what());
        }
    }

    py::object load_attribute_by_name(const std::string& name) const {
        if (!ptr) throw std::runtime_error("Null pointer in load_attribute_by_name");
        try {
            int index = find_attribute(name);
            if (index < 0) {
                throw std::runtime_error("Attribute not found: " + name);
            }
            return load_attribute_by_index(index);
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in load_attribute_by_name: ") + e.what());
        }
    }

    py::object load_vec_element(int index) const {
        if (!ptr) throw std::runtime_error("Null pointer in load_vec_element");
        try {
            if (ptr->type() != rds2cpp::SEXPType::VEC) {
                throw std::runtime_error("Not a vector type");
            }
            const auto& data = static_cast<const rds2cpp::GenericVector*>(ptr)->data;
            if (index < 0 || static_cast<size_t>(index) >= data.size()) {
                throw std::out_of_range("Vector index out of range");
            }
            return py::cast(new RdsReader(data[index].get()));
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in load_vec_element: ") + e.what());
        }
    }

    std::string get_package_name() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_package_name");
        try {
            if (ptr->type() != rds2cpp::SEXPType::S4) {
                throw std::runtime_error("Not an S4 object");
            }
            return static_cast<const rds2cpp::S4Object*>(ptr)->package_name;
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_package_name: ") + e.what());
        }
    }

    std::string get_class_name() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_class_name");
        try {
            if (ptr->type() != rds2cpp::SEXPType::S4) {
                throw std::runtime_error("Not an S4 object");
            }
            return static_cast<const rds2cpp::S4Object*>(ptr)->class_name;
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_class_name: ") + e.what());
        }
    }

    std::pair<size_t, size_t> get_dimensions() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_dimensions");
        try {
            if (ptr->type() != rds2cpp::SEXPType::INT) {
                throw std::runtime_error("Dimensions must be integer");
            }
            const auto& dims = static_cast<const rds2cpp::IntegerVector*>(ptr)->data;
            if (dims.size() != 2 || dims[0] < 0 || dims[1] < 0) {
                throw std::runtime_error("Invalid dimensions");
            }
            return {static_cast<size_t>(dims[0]), static_cast<size_t>(dims[1])};
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_dimensions: ") + e.what());
        }
    }

private:
    const rds2cpp::Attributes& get_attributes() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_attributes");
        try {
            switch (ptr->type()) {
                case rds2cpp::SEXPType::INT: return static_cast<const rds2cpp::IntegerVector*>(ptr)->attributes;
                case rds2cpp::SEXPType::REAL: return static_cast<const rds2cpp::DoubleVector*>(ptr)->attributes;
                case rds2cpp::SEXPType::LGL: return static_cast<const rds2cpp::LogicalVector*>(ptr)->attributes;
                case rds2cpp::SEXPType::STR: return static_cast<const rds2cpp::StringVector*>(ptr)->attributes;
                case rds2cpp::SEXPType::VEC: return static_cast<const rds2cpp::GenericVector*>(ptr)->attributes;
                case rds2cpp::SEXPType::S4: return static_cast<const rds2cpp::S4Object*>(ptr)->attributes;
                default: throw std::runtime_error("Unsupported type for attributes");
            }
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in get_attributes: ") + e.what());
        }
    }
};

class RdsObject {
private:
    std::unique_ptr<rds2cpp::Parsed> parsed;
    std::unique_ptr<RdsReader> reader;

public:
    RdsObject(const std::string& file) {
        try {
            parsed = std::make_unique<rds2cpp::Parsed>(rds2cpp::parse_rds(file));
            if (!parsed || !parsed->object) {
                throw std::runtime_error("Failed to parse RDS file");
            }
            reader = std::make_unique<RdsReader>(parsed->object.get());
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in RdsObject constructor: ") + e.what());
        }
    }

    RdsReader* get_robject() const {
        if (!reader) throw std::runtime_error("Null reader in get_robject");
        return reader.get();
    }
};

PYBIND11_MODULE(rds_parser, m) {
    py::register_exception<std::runtime_error>(m, "RdsParserError");

    py::class_<RdsObject>(m, "RdsObject")
        .def(py::init<const std::string&>())
        .def("get_robject", &RdsObject::get_robject, py::return_value_policy::reference_internal);

    py::class_<RdsReader>(m, "RdsReader")
        .def(py::init<const rds2cpp::RObject*>())
        .def("get_rtype", &RdsReader::get_rtype)
        .def("get_rsize", &RdsReader::get_rsize)
        .def("realize_value", &RdsReader::realize_value)
        .def("get_int_or_bool_arr", &RdsReader::get_int_or_bool_arr)
        .def("get_double_arr", &RdsReader::get_double_arr)
        .def("get_string_arr", &RdsReader::get_string_arr)
        .def("get_vector_arr", &RdsReader::get_vector_arr)
        .def("get_attribute_names", &RdsReader::get_attribute_names)
        .def("find_attribute", &RdsReader::find_attribute)
        .def("load_attribute_by_index", &RdsReader::load_attribute_by_index)
        .def("load_attribute_by_name", &RdsReader::load_attribute_by_name)
        .def("load_vec_element", &RdsReader::load_vec_element)
        .def("get_package_name", &RdsReader::get_package_name)
        .def("get_class_name", &RdsReader::get_class_name)
        .def("get_dimensions", &RdsReader::get_dimensions);
}