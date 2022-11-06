"""
    Setup file for rds2py.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize
import numpy

if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            ext_modules=cythonize(
                [
                    Extension(
                        "rds2py.core",
                        ["src/rds2py/lib/rds_parser.cpp", "src/rds2py/lib/parser.pyx"],
                        include_dirs=["extern/rds2cpp/include", "extern/rds2cpp/_deps/byteme-src/include", numpy.get_include()],
                        language="c++",
                        extra_compile_args=[
                           "-std=c++17",
                        ],
                        extra_link_args = ["-lz"]
                    )
                ],
                compiler_directives={"language_level": "3"},
            ),
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
