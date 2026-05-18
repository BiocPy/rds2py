#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <rds2cpp/rds2cpp.hpp>
#include <stdexcept>
#include <pybind11/iostream.h>

namespace py = pybind11;

class RdsReader {
private:
    const rds2cpp::RObject* ptr;
    const std::vector<rds2cpp::Symbol>* symbols_ptr;

public:
    RdsReader(const rds2cpp::RObject* p, const std::vector<rds2cpp::Symbol>* syms) : ptr(p), symbols_ptr(syms) {
        if (!p) throw std::runtime_error("Null pointer passed to 'RdsReader'.");
        if (!syms) throw std::runtime_error("Null symbols pointer passed to 'RdsReader'.");
    }

    std::string get_rtype() const {
        if (!ptr) throw std::runtime_error("Null pointer in 'get_rtype'.");
        // py::print("arg::", static_cast<int>(ptr->type()));
        switch (ptr->type()) {
            case rds2cpp::SEXPType::S4: return "S4";
            case rds2cpp::SEXPType::INT: return "integer";
            case rds2cpp::SEXPType::REAL: return "double";
            case rds2cpp::SEXPType::STR: return "string";
            case rds2cpp::SEXPType::LGL: return "boolean";
            case rds2cpp::SEXPType::VEC: return "vector";
            case rds2cpp::SEXPType::NIL: return "null";
            default: return "other";
        }
    }

    int get_rsize() const {
        if (!ptr) throw std::runtime_error("Null pointer in 'get_rsize'.");
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT: return static_cast<const rds2cpp::IntegerVector*>(ptr)->data.size();
            case rds2cpp::SEXPType::REAL: return static_cast<const rds2cpp::DoubleVector*>(ptr)->data.size();
            case rds2cpp::SEXPType::STR: return static_cast<const rds2cpp::StringVector*>(ptr)->data.size();
            case rds2cpp::SEXPType::LGL: return static_cast<const rds2cpp::LogicalVector*>(ptr)->data.size();
            case rds2cpp::SEXPType::VEC: return static_cast<const rds2cpp::GenericVector*>(ptr)->data.size();
            default: return -1;
        }
    }

    py::array get_numeric_data() const {
        if (!ptr) throw std::runtime_error("Null pointer in 'get_numeric_data'.");
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT: {
                const auto& data = static_cast<const rds2cpp::IntegerVector*>(ptr)->data;
                return py::array_t<int32_t>({data.size()}, {sizeof(int32_t)}, data.data());
            }
            case rds2cpp::SEXPType::LGL: {
                const auto& data = static_cast<const rds2cpp::LogicalVector*>(ptr)->data;
                return py::array_t<int32_t>({data.size()}, {sizeof(int32_t)}, data.data());
            }
            case rds2cpp::SEXPType::REAL: {
                const auto& data = static_cast<const rds2cpp::DoubleVector*>(ptr)->data;
                return py::array_t<double>({data.size()}, {sizeof(double)}, data.data());
            }
            default:
                throw std::runtime_error("Invalid type for numeric data");
        }
    }

    py::list get_string_arr() const {
        if (!ptr) throw std::runtime_error("Null pointer in 'get_string_arr'.");
        if (ptr->type() != rds2cpp::SEXPType::STR) {
            throw std::runtime_error("Invalid type for 'string_arr'");
        }
        const auto& data = static_cast<const rds2cpp::StringVector*>(ptr)->data;
        py::list result;
        for (const auto& s : data) {
            if (s.value.has_value()) {
                result.append(s.value.value());
            } else {
                result.append(py::none());
            }
        }
        return result;
    }

    py::list get_attribute_names() const {
        if (!ptr) throw std::runtime_error("Null pointer in 'get_attribute_names'");
        const auto& attrs = get_attributes();
        py::list names;
        for (const auto& attr : attrs) {
            names.append(resolve_symbol(attr.name));
        }
        return names;
    }

    py::object load_attribute_by_name(const std::string& name) const {
        if (!ptr) throw std::runtime_error("Null pointer in 'load_attribute_by_name'");
        const auto& attrs = get_attributes();
        for (const auto& attr : attrs) {
            if (resolve_symbol(attr.name) == name) {
                return py::cast(new RdsReader(attr.value.get(), symbols_ptr));
            }
        }
        throw std::runtime_error("Attribute not found: " + name);
    }

    py::object load_vec_element(int index) const {
        if (!ptr) throw std::runtime_error("Null pointer in 'load_vec_element'");
        if (ptr->type() != rds2cpp::SEXPType::VEC) {
            throw std::runtime_error("Not a vector type");
        }
        const auto& data = static_cast<const rds2cpp::GenericVector*>(ptr)->data;
        if (index < 0 || static_cast<size_t>(index) >= data.size()) {
            throw std::out_of_range("Vector index out of range");
        }
        return py::cast(new RdsReader(data[index].get(), symbols_ptr));
    }

    std::string get_package_name() const {
        if (!ptr || ptr->type() != rds2cpp::SEXPType::S4) {
            throw std::runtime_error("Not an S4 object");
        }
        return static_cast<const rds2cpp::S4Object*>(ptr)->package_name;
    }

    std::string get_class_name() const {
        if (!ptr || ptr->type() != rds2cpp::SEXPType::S4) {
            throw std::runtime_error("Not an S4 object");
        }
        return static_cast<const rds2cpp::S4Object*>(ptr)->class_name;
    }

    std::pair<size_t, size_t> get_dimensions() const {
        if (!ptr || ptr->type() != rds2cpp::SEXPType::INT) {
            throw std::runtime_error("Dimensions must be integer");
        }
        const auto& dims = static_cast<const rds2cpp::IntegerVector*>(ptr)->data;
        if (dims.size() != 2 || dims[0] < 0 || dims[1] < 0) {
            throw std::runtime_error("Invalid dimensions");
        }
        return {static_cast<size_t>(dims[0]), static_cast<size_t>(dims[1])};
    }

private:
    std::string resolve_symbol(const rds2cpp::SymbolIndex& sym) const {
        if (sym.index >= symbols_ptr->size()) {
            throw std::runtime_error("Symbol index out of range");
        }
        return (*symbols_ptr)[sym.index].name;
    }

    const std::vector<rds2cpp::Attribute>& get_attributes() const {
        if (!ptr) throw std::runtime_error("Null pointer in get_attributes");
        switch (ptr->type()) {
            case rds2cpp::SEXPType::INT: return static_cast<const rds2cpp::IntegerVector*>(ptr)->attributes;
            case rds2cpp::SEXPType::REAL: return static_cast<const rds2cpp::DoubleVector*>(ptr)->attributes;
            case rds2cpp::SEXPType::LGL: return static_cast<const rds2cpp::LogicalVector*>(ptr)->attributes;
            case rds2cpp::SEXPType::STR: return static_cast<const rds2cpp::StringVector*>(ptr)->attributes;
            case rds2cpp::SEXPType::VEC: return static_cast<const rds2cpp::GenericVector*>(ptr)->attributes;
            case rds2cpp::SEXPType::S4: return static_cast<const rds2cpp::S4Object*>(ptr)->attributes;
            default: throw std::runtime_error("Unsupported type for attributes");
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
            rds2cpp::ParseRdsOptions options;
            parsed = std::make_unique<rds2cpp::Parsed>(rds2cpp::parse_rds(file, options));
            if (!parsed || !parsed->object) {
                throw std::runtime_error("Failed to parse RDS file");
            }
            reader = std::make_unique<RdsReader>(parsed->object.get(), &parsed->symbols);
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in 'RdsObject' constructor: ") + e.what());
        }
    }

    RdsReader* get_robject() const {
        if (!reader) throw std::runtime_error("Null reader in 'get_robject'");
        return reader.get();
    }
};

class RdaObject {
private:
    std::unique_ptr<rds2cpp::RdaFile> parsed;

public:
    RdaObject(const std::string& file) {
        try {
            rds2cpp::ParseRdaOptions options;
            parsed = std::make_unique<rds2cpp::RdaFile>(rds2cpp::parse_rda(file, options));
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in 'RdaObject' constructor: ") + e.what());
        }
    }

    py::list get_object_names() const {
        if (!parsed) throw std::runtime_error("Null parsed in 'get_object_names'");
        py::list names;
        for (const auto& obj : parsed->objects) {
            if (obj.name.index < parsed->symbols.size()) {
                names.append(parsed->symbols[obj.name.index].name);
            } else {
                names.append(py::none());
            }
        }
        return names;
    }

    int get_object_count() const {
        if (!parsed) throw std::runtime_error("Null parsed in 'get_object_count'");
        return static_cast<int>(parsed->objects.size());
    }

    RdsReader* get_object_by_index(int index) const {
        if (!parsed) throw std::runtime_error("Null parsed in 'get_object_by_index'");
        if (index < 0 || static_cast<size_t>(index) >= parsed->objects.size()) {
            throw std::out_of_range("Object index out of range");
        }
        return new RdsReader(parsed->objects[index].value.get(), &parsed->symbols);
    }

    RdsReader* get_object_by_name(const std::string& name) const {
        if (!parsed) throw std::runtime_error("Null parsed in 'get_object_by_name'");
        for (const auto& obj : parsed->objects) {
            if (obj.name.index < parsed->symbols.size() &&
                parsed->symbols[obj.name.index].name == name) {
                return new RdsReader(obj.value.get(), &parsed->symbols);
            }
        }
        throw std::runtime_error("Object not found: " + name);
    }
};

PYBIND11_MODULE(lib_rds_parser, m) {
    py::register_exception<std::runtime_error>(m, "RdsParserError");

    py::class_<RdsObject>(m, "RdsObject")
        .def(py::init<const std::string&>())
        .def("get_robject", &RdsObject::get_robject, py::return_value_policy::reference_internal);

    py::class_<RdaObject>(m, "RdaObject")
        .def(py::init<const std::string&>())
        .def("get_object_names", &RdaObject::get_object_names)
        .def("get_object_count", &RdaObject::get_object_count)
        .def("get_object_by_index", &RdaObject::get_object_by_index, py::return_value_policy::take_ownership, py::keep_alive<0, 1>())
        .def("get_object_by_name", &RdaObject::get_object_by_name, py::return_value_policy::take_ownership, py::keep_alive<0, 1>());

    py::class_<RdsReader>(m, "RdsReader")
        .def("get_rtype", &RdsReader::get_rtype)
        .def("get_rsize", &RdsReader::get_rsize)
        .def("get_numeric_data", &RdsReader::get_numeric_data)
        .def("get_string_arr", &RdsReader::get_string_arr)
        .def("get_attribute_names", &RdsReader::get_attribute_names)
        .def("load_attribute_by_name", &RdsReader::load_attribute_by_name)
        .def("load_vec_element", &RdsReader::load_vec_element)
        .def("get_package_name", &RdsReader::get_package_name)
        .def("get_class_name", &RdsReader::get_class_name)
        .def("get_dimensions", &RdsReader::get_dimensions);
}
