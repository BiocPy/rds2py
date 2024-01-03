[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/rds2py.svg)](https://pypi.org/project/rds2py/)
![Unit tests](https://github.com/BiocPy/rds2py/actions/workflows/pypi-test.yml/badge.svg)

# rds2py

Parse and construct Python representations for datasets stored in RDS files. `rds2py` supports a few base classes from R and Bioconductor's `SummarizedExperiment` and `SingleCellExperiment` S4 classes. **_This is possible because of [Aaron's rds2cpp library](https://github.com/LTLA/rds2cpp)._**

The package uses memory views (except for strings) to access the same memory from C++ in Python (through Cython of course). This is especially useful for large datasets so we don't make multiple copies of data.

## Install

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py
```

## Usage

If you do not have an RDS object handy, feel free to download one from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

```python
from rds2py import as_summarized_experiment, read_rds

r_obj = read_rds(<path_to_file>)
```

This `r_obj` holds a dictionary representation of the RDS file, we can now transform this object into Python representations.

`rObj` always contains two keys

- `data`: If atomic entities, contains the NumPy view of the array.
- `attributes`: Additional properties available for the object.

In addition, the package provides functions to convert parsed R objects into Python representations.

```python
from rds2py import as_spase_matrix, as_summarized_experiment

# to convert an robject to a sparse matrix
sp_mat = as_sparse(rObj)

# to convert an robject to SCE
sce = as_summarized_experiment(rObj)
```

For more examples converting `data.frame`, `dgCMatrix`, `dgRMatrix`, `dgTMatrix` to Python, checkout the [documentation](https://biocpy.github.io/rds2py/).

## Developer Notes

This project uses Cython to provide bindings from C++ to Python.

Steps to setup dependencies -

- git submodules is initialized in `extern/rds2cpp`
- `cmake .` in `extern/rds2cpp` directory to download dependencies, especially the `byteme` library

First one needs to build the extern library, this would generate a shared object file to `src/rds2py/core-[*].so`

```shell
python setup.py build_ext --inplace
```

For typical development workflows, run

```shell
python setup.py build_ext --inplace && tox
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
