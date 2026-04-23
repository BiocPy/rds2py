cmake_minimum_required(VERSION 3.24)

project(rds2py
    VERSION 1.0.0
    DESCRIPTION "Building the rds shared library"
    LANGUAGES C CXX)

# Importing all of the dependencies with pinned versions (even for transitive dependencies).
include(FetchContent)

# On Windows (or when zlib is not found), build zlib from source so that
# byteme can use GzipFileReader / GzipFileWriter.
find_package(ZLIB QUIET)
if(NOT ZLIB_FOUND)
    message(STATUS "System zlib not found -- building zlib from source via FetchContent")
    FetchContent_Declare(
      zlib
      GIT_REPOSITORY https://github.com/madler/zlib
      GIT_TAG v1.3.1
    )
    set(ZLIB_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(zlib)

    # Make the zlib headers visible to downstream targets and set the
    # ZLIB_FOUND / ZLIB::ZLIB variables that byteme's CMakeLists.txt looks for.
    add_library(ZLIB::ZLIB ALIAS zlibstatic)
    target_include_directories(zlibstatic PUBLIC
        "${zlib_SOURCE_DIR}"
        "${zlib_BINARY_DIR}"
    )
    set(ZLIB_FOUND TRUE CACHE BOOL "" FORCE)
    set(ZLIB_LIBRARIES zlibstatic CACHE STRING "" FORCE)
    set(ZLIB_INCLUDE_DIRS "${zlib_SOURCE_DIR};${zlib_BINARY_DIR}" CACHE STRING "" FORCE)
endif()

FetchContent_Declare(
  rds2cpp
  GIT_REPOSITORY https://github.com/LTLA/rds2cpp
  GIT_TAG master
)

FetchContent_Declare(
  byteme
  GIT_REPOSITORY https://github.com/LTLA/byteme
  GIT_TAG master
)

FetchContent_Declare(
  sanisizer
  GIT_REPOSITORY https://github.com/LTLA/sanisizer
  GIT_TAG master
)

FetchContent_MakeAvailable(byteme)
FetchContent_MakeAvailable(sanisizer)
FetchContent_MakeAvailable(rds2cpp)

# Defining the targets.
set(TARGET rds2py)

find_package(pybind11 CONFIG)

# pybind11 method:
pybind11_add_module(${TARGET}
    src/rdswrapper.cpp
)

set_property(TARGET ${TARGET} PROPERTY CXX_STANDARD 17)

target_link_libraries(${TARGET} PRIVATE rds2cpp pybind11::pybind11)

# On Windows, also link zlib so the gzip symbols are available at link time.
if(NOT ZLIB_FOUND OR TARGET zlibstatic)
    target_link_libraries(${TARGET} PRIVATE ZLIB::ZLIB)
endif()

set_target_properties(${TARGET} PROPERTIES
    OUTPUT_NAME lib_rds_parser
    PREFIX ""
)
