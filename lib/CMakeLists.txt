cmake_minimum_required(VERSION 3.24)

project(rds2py
    VERSION 1.0.0
    DESCRIPTION "Building the rds shared library"
    LANGUAGES CXX)

# Importing all of the dependencies with pinned versions (even for transitive dependencies).
include(FetchContent)

FetchContent_Declare(
  rds2cpp
  GIT_REPOSITORY https://github.com/LTLA/rds2cpp
  GIT_TAG v1.1.0
)

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

set_target_properties(${TARGET} PROPERTIES
    OUTPUT_NAME lib_rds_parser
    PREFIX ""
)
