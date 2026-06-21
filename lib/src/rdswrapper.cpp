#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <rds2cpp/rds2cpp.hpp>
#include <stdexcept>
#include <pybind11/iostream.h>
#include <limits>

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
        switch (ptr->type()) {
            case rds2cpp::SEXPType::S4: return "S4";
            case rds2cpp::SEXPType::INT: return "integer";
            case rds2cpp::SEXPType::REAL: return "double";
            case rds2cpp::SEXPType::STR: return "string";
            case rds2cpp::SEXPType::LGL: return "boolean";
            case rds2cpp::SEXPType::VEC: return "vector";
            case rds2cpp::SEXPType::NIL: return "null";
            case rds2cpp::SEXPType::SYM: return "symbol";
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

    std::string get_symbol_name() const {
        if (!ptr || ptr->type() != rds2cpp::SEXPType::SYM) {
            throw std::runtime_error("Not a symbol object");
        }
        const auto* sym = static_cast<const rds2cpp::SymbolIndex*>(ptr);
        if (sym->index >= symbols_ptr->size()) {
            throw std::runtime_error("Symbol index out of range");
        }
        return (*symbols_ptr)[sym->index].name;
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

// ---- writers ----

std::unique_ptr<rds2cpp::RObject> py_to_robject(const py::object& obj, std::vector<rds2cpp::Symbol>& symbols);

void add_names_attribute(
    std::vector<rds2cpp::Attribute>& attributes,
    const py::list& names,
    std::vector<rds2cpp::Symbol>& symbols)
{
    auto svec = std::make_unique<rds2cpp::StringVector>();
    for (size_t i = 0; i < py::len(names); ++i) {
        auto item = names[i];
        if (item.is_none()) {
            svec->data.emplace_back();
        } else {
            svec->data.emplace_back(item.cast<std::string>(), rds2cpp::StringEncoding::UTF8);
        }
    }
    attributes.emplace_back(
        rds2cpp::register_symbol("names", rds2cpp::StringEncoding::UTF8, symbols),
                            std::move(svec)
    );
}

std::unique_ptr<rds2cpp::RObject> py_to_robject(const py::object& obj, std::vector<rds2cpp::Symbol>& symbols) {
    // None -> Null
    if (obj.is_none()) {
        return std::make_unique<rds2cpp::Null>();
    }

    // numpy array
    if (py::isinstance<py::array>(obj)) {
        auto arr = obj.cast<py::array>();
        auto dtype = arr.dtype();

        // bool arrays
        if (dtype.is(py::dtype::of<bool>())) {
            auto buf = arr.cast<py::array_t<bool, py::array::c_style | py::array::forcecast>>();
            auto r = buf.unchecked<1>();
            auto vec = std::make_unique<rds2cpp::LogicalVector>();

            vec->data.reserve(r.shape(0));
            for (ssize_t i = 0; i < r.shape(0); ++i) {
                vec->data.push_back(r(i) ? 1 : 0);
            }

            return vec;
        }

        // integer arrays
        if (py::isinstance<py::array_t<int32_t>>(arr) ||
            py::isinstance<py::array_t<int64_t>>(arr) ||
            py::isinstance<py::array_t<int16_t>>(arr) ||
            py::isinstance<py::array_t<int8_t>>(arr)) {
            auto buf = arr.cast<py::array_t<int32_t, py::array::c_style | py::array::forcecast>>();
            auto r = buf.unchecked<1>();
            auto vec = std::make_unique<rds2cpp::IntegerVector>();

            vec->data.reserve(r.shape(0));
            for (ssize_t i = 0; i < r.shape(0); ++i) {
                vec->data.push_back(r(i));
            }

            return vec;
        }

        // float arrays
        if (py::isinstance<py::array_t<double>>(arr) ||
            py::isinstance<py::array_t<float>>(arr)) {
            auto buf = arr.cast<py::array_t<double, py::array::c_style | py::array::forcecast>>();
            auto r = buf.unchecked<1>();
            auto vec = std::make_unique<rds2cpp::DoubleVector>();

            vec->data.reserve(r.shape(0));
            for (ssize_t i = 0; i < r.shape(0); ++i) {
                vec->data.push_back(r(i));
            }
            return vec;
        }

        throw std::runtime_error("Unsupported numpy dtype for RDS writing");
    }

    // dict
    if (py::isinstance<py::dict>(obj)) {
        auto d = obj.cast<py::dict>();

        // If it's a structured R object dictionary:
        if (d.contains("type")) {
            std::string rtype = d["type"].cast<std::string>();

            if (rtype == "S4") {
                auto s4 = std::make_unique<rds2cpp::S4Object>();
                s4->class_name = d["class_name"].cast<std::string>();
                s4->package_name = d["package_name"].cast<std::string>();
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        py::object val_py = py::reinterpret_borrow<py::object>(item.second);
                        std::unique_ptr<rds2cpp::RObject> val_obj;
                        if (val_py.is_none()) {
                            val_obj = std::make_unique<rds2cpp::SymbolIndex>(
                                rds2cpp::register_symbol("\001NULL\001", rds2cpp::StringEncoding::UTF8, symbols)
                            );
                        } else if (py::isinstance<py::dict>(val_py) && val_py.cast<py::dict>().contains("type") && py::isinstance<py::str>(val_py.cast<py::dict>()["type"]) && val_py.cast<py::dict>()["type"].cast<std::string>() == "null") {
                            val_obj = std::make_unique<rds2cpp::SymbolIndex>(
                                rds2cpp::register_symbol("\001NULL\001", rds2cpp::StringEncoding::UTF8, symbols)
                            );
                        } else {
                            val_obj = py_to_robject(val_py, symbols);
                        }
                        s4->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return s4;
            }

            if (rtype == "integer") {
                auto vec = std::make_unique<rds2cpp::IntegerVector>();
                if (d.contains("data") && !d["data"].is_none()) {
                    auto data_obj = d["data"];
                    if (py::isinstance<py::array>(data_obj)) {
                        auto arr = data_obj.cast<py::array_t<int32_t, py::array::c_style | py::array::forcecast>>();
                        auto r = arr.unchecked<1>();
                        vec->data.reserve(r.shape(0));
                        for (ssize_t i = 0; i < r.shape(0); ++i) vec->data.push_back(r(i));
                    } else {
                        auto seq = data_obj.cast<py::sequence>();
                        vec->data.reserve(py::len(seq));
                        for (size_t i = 0; i < py::len(seq); ++i) {
                            if (seq[i].is_none()) {
                                vec->data.push_back(-2147483648);
                            } else {
                                vec->data.push_back(seq[i].cast<int32_t>());
                            }
                        }
                    }
                }
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        auto val_obj = py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols);
                        vec->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return vec;
            }

            if (rtype == "double" || rtype == "numeric") {
                auto vec = std::make_unique<rds2cpp::DoubleVector>();
                if (d.contains("data") && !d["data"].is_none()) {
                    auto data_obj = d["data"];
                    if (py::isinstance<py::array>(data_obj)) {
                        auto arr = data_obj.cast<py::array_t<double, py::array::c_style | py::array::forcecast>>();
                        auto r = arr.unchecked<1>();
                        vec->data.reserve(r.shape(0));
                        for (ssize_t i = 0; i < r.shape(0); ++i) vec->data.push_back(r(i));
                    } else {
                        auto seq = data_obj.cast<py::sequence>();
                        vec->data.reserve(py::len(seq));
                        for (size_t i = 0; i < py::len(seq); ++i) {
                            if (seq[i].is_none()) {
                                vec->data.push_back(std::numeric_limits<double>::quiet_NaN());
                            } else {
                                vec->data.push_back(seq[i].cast<double>());
                            }
                        }
                    }
                }
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        auto val_obj = py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols);
                        vec->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return vec;
            }

            if (rtype == "boolean" || rtype == "logical") {
                auto vec = std::make_unique<rds2cpp::LogicalVector>();
                if (d.contains("data") && !d["data"].is_none()) {
                    auto data_obj = d["data"];
                    if (py::isinstance<py::array>(data_obj)) {
                        auto arr = data_obj.cast<py::array_t<bool, py::array::c_style | py::array::forcecast>>();
                        auto r = arr.unchecked<1>();
                        vec->data.reserve(r.shape(0));
                        for (ssize_t i = 0; i < r.shape(0); ++i) vec->data.push_back(r(i) ? 1 : 0);
                    } else {
                        auto seq = data_obj.cast<py::sequence>();
                        vec->data.reserve(py::len(seq));
                        for (size_t i = 0; i < py::len(seq); ++i) {
                            if (seq[i].is_none()) {
                                vec->data.push_back(-2147483648);
                            } else {
                                vec->data.push_back(seq[i].cast<bool>() ? 1 : 0);
                            }
                        }
                    }
                }
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        auto val_obj = py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols);
                        vec->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return vec;
            }

            if (rtype == "string" || rtype == "character") {
                auto vec = std::make_unique<rds2cpp::StringVector>();
                if (d.contains("data") && !d["data"].is_none()) {
                    auto lst = d["data"].cast<py::list>();
                    vec->data.reserve(py::len(lst));
                    for (size_t i = 0; i < py::len(lst); ++i) {
                        auto item = lst[i];
                        if (item.is_none()) {
                            vec->data.emplace_back();
                        } else {
                            vec->data.emplace_back(item.cast<std::string>(), rds2cpp::StringEncoding::UTF8);
                        }
                    }
                }
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        auto val_obj = py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols);
                        vec->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return vec;
            }

            if (rtype == "vector" || rtype == "list") {
                auto vec = std::make_unique<rds2cpp::GenericVector>();
                if (d.contains("data") && !d["data"].is_none()) {
                    auto lst = d["data"].cast<py::list>();
                    vec->data.reserve(py::len(lst));
                    for (size_t i = 0; i < py::len(lst); ++i) {
                        vec->data.push_back(py_to_robject(lst[i].cast<py::object>(), symbols));
                    }
                }
                if (d.contains("attributes") && !d["attributes"].is_none()) {
                    auto attrs = d["attributes"].cast<py::dict>();
                    for (auto& item : attrs) {
                        auto name_str = item.first.cast<std::string>();
                        auto name_sym = rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols);
                        auto val_obj = py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols);
                        vec->attributes.emplace_back(name_sym, std::move(val_obj));
                    }
                }
                return vec;
            }

            if (rtype == "symbol") {
                std::string name_str = d["name"].cast<std::string>();
                return std::make_unique<rds2cpp::SymbolIndex>(
                    rds2cpp::register_symbol(name_str, rds2cpp::StringEncoding::UTF8, symbols)
                );
            }

            if (rtype == "null") {
                return std::make_unique<rds2cpp::Null>();
            }

            throw std::runtime_error("Unsupported type for structured RDS writing: " + rtype);
        }

        // Default dictionary -> GenericVector with names attribute
        auto gvec = std::make_unique<rds2cpp::GenericVector>();
        py::list keys;
        for (auto& item : d) {
            keys.append(item.first);
            gvec->data.push_back(py_to_robject(py::reinterpret_borrow<py::object>(item.second), symbols));
        }
        add_names_attribute(gvec->attributes, keys, symbols);
        return gvec;
    }

    //  list
    if (py::isinstance<py::list>(obj)) {
        auto lst = obj.cast<py::list>();
        if (py::len(lst) == 0) {
            return std::make_unique<rds2cpp::GenericVector>();
        }

        // Check if all elements are strings (or None) -> StringVector
        bool all_strings = true;
        for (size_t i = 0; i < py::len(lst); ++i) {
            auto item = lst[i];
            if (!item.is_none() && !py::isinstance<py::str>(item)) {
                all_strings = false;
                break;
            }
        }

        if (all_strings) {
            auto svec = std::make_unique<rds2cpp::StringVector>();
            for (size_t i = 0; i < py::len(lst); ++i) {
                auto item = lst[i];
                if (item.is_none()) {
                    svec->data.emplace_back();
                } else {
                    svec->data.emplace_back(item.cast<std::string>(), rds2cpp::StringEncoding::UTF8);
                }
            }

            return svec;
        }

        // Otherwise -> GenericVector
        auto gvec = std::make_unique<rds2cpp::GenericVector>();
        for (size_t i = 0; i < py::len(lst); ++i) {
            gvec->data.push_back(py_to_robject(lst[i].cast<py::object>(), symbols));
        }

        return gvec;
    }

    // bool check before int, since bool is a subclass of int
    if (py::isinstance<py::bool_>(obj)) {
        auto vec = std::make_unique<rds2cpp::LogicalVector>();
        vec->data.push_back(obj.cast<bool>() ? 1 : 0);
        return vec;
    }

    if (py::isinstance<py::int_>(obj)) {
        auto vec = std::make_unique<rds2cpp::IntegerVector>();
        vec->data.push_back(obj.cast<int32_t>());
        return vec;
    }

    if (py::isinstance<py::float_>(obj)) {
        auto vec = std::make_unique<rds2cpp::DoubleVector>();
        vec->data.push_back(obj.cast<double>());
        return vec;
    }

    if (py::isinstance<py::str>(obj)) {
        auto svec = std::make_unique<rds2cpp::StringVector>();
        svec->data.emplace_back(obj.cast<std::string>(), rds2cpp::StringEncoding::UTF8);
        return svec;
    }

    throw std::runtime_error("Unsupported Python type for RDS writing: " + std::string(py::str(obj.get_type())));
}

void write_rds_file(const py::object& obj, const std::string& path) {
    rds2cpp::RdsFile file_info;
    file_info.object = py_to_robject(obj, file_info.symbols);
    rds2cpp::WriteRdsOptions options;
    rds2cpp::write_rds(file_info, path, options);
}

void write_rda_file(const py::dict& objects, const std::string& path) {
    rds2cpp::RdaFile file_info;
    for (auto& item : objects) {
        auto name = item.first.cast<std::string>();
        auto sym = rds2cpp::register_symbol(name, rds2cpp::StringEncoding::UTF8, file_info.symbols);
        auto value = py_to_robject(py::reinterpret_borrow<py::object>(item.second), file_info.symbols);
        file_info.objects.emplace_back(std::move(sym), std::move(value));
    }
    rds2cpp::WriteRdaOptions options;
    rds2cpp::write_rda(file_info, path, options);
}

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
    .def("get_dimensions", &RdsReader::get_dimensions)
    .def("get_symbol_name", &RdsReader::get_symbol_name);

    m.def("write_rds", &write_rds_file, "Write a Python object to an RDS file",
        py::arg("obj"), py::arg("path"));

    m.def("write_rda", &write_rda_file, "Write named Python objects to an RData file",
        py::arg("objects"), py::arg("path"));
}
