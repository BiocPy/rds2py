"""Setup file for rds2py. Use setup.cfg to configure your project.

This file was generated with PyScaffold 4.5.
PyScaffold helps you to put up the scaffold of your new Python project.
Learn more under: https://pyscaffold.org/
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
import pathlib
import os
import shutil
import sys
import pybind11


###  Adapted from dolomite_base: https://github.com/ArtifactDB/dolomite-base/blob/master/setup.py
## Adapted from https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py.
class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        build_temp = pathlib.Path(self.build_temp)
        build_lib = pathlib.Path(self.build_lib)
        outpath = os.path.join(build_lib.absolute(), ext.name)

        if not os.path.exists(build_temp):
            cmd = [
                "cmake",
                "-S",
                "lib",
                "-B",
                build_temp,
                "-Dpybind11_DIR=" + os.path.join(os.path.dirname(pybind11.__file__), "share", "cmake", "pybind11"),
                "-DPYTHON_EXECUTABLE=" + sys.executable,
            ]
            if os.name != "nt":
                cmd.append("-DCMAKE_BUILD_TYPE=Release")
                cmd.append("-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + outpath)

            if "MORE_CMAKE_OPTIONS" in os.environ:
                cmd += os.environ["MORE_CMAKE_OPTIONS"].split()
            self.spawn(cmd)

        if not self.dry_run:
            cmd = ["cmake", "--build", build_temp]
            if os.name == "nt":
                cmd += ["--config", "Release"]
            self.spawn(cmd)
            if os.name == "nt":
                # Gave up trying to get MSVC to respect the output directory.
                # Delvewheel also needs it to have a 'pyd' suffix... whatever.
                shutil.copyfile(
                    os.path.join(build_temp, "Release", "_core.dll"),
                    os.path.join(outpath, "_core.pyd"),
                )


if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            ext_modules=[CMakeExtension("rds2py")],
            cmdclass={"build_ext": build_ext},
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
