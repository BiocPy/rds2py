/* DO NOT MODIFY: this is automatically generated by the cpptypes */

#include <cstring>
#include <stdexcept>
#include <cstdint>

#ifdef _WIN32
#define PYAPI __declspec(dllexport)
#else
#define PYAPI
#endif

static char* copy_error_message(const char* original) {
    auto n = std::strlen(original);
    auto copy = new char[n + 1];
    std::strcpy(copy, original);
    return copy;
}

inline uintptr_t py_parser_extract_robject(uintptr_t);

inline uintptr_t py_parser_rds_file(std::string);

extern "C" {

PYAPI void free_error_message(char** msg) {
    delete [] *msg;
}

PYAPI inline uintptr_t py_py_parser_extract_robject(uintptr_t ptr, int32_t* errcode, char** errmsg) {
    inline uintptr_t output = 0;
    try {
        output = py_parser_extract_robject(ptr);
    } catch(std::exception& e) {
        *errcode = 1;
        *errmsg = copy_error_message(e.what());
    } catch(...) {
        *errcode = 1;
        *errmsg = copy_error_message("unknown C++ exception");
    }
    return output;
}

PYAPI inline uintptr_t py_py_parser_rds_file(std::string file, int32_t* errcode, char** errmsg) {
    inline uintptr_t output = 0;
    try {
        output = py_parser_rds_file(file);
    } catch(std::exception& e) {
        *errcode = 1;
        *errmsg = copy_error_message(e.what());
    } catch(...) {
        *errcode = 1;
        *errmsg = copy_error_message("unknown C++ exception");
    }
    return output;
}

}