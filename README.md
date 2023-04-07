# rds2py

Parse and construct Python representations for datasets stored in RDS files. It supports a few base classes from R and Bioconductor's `SummarizedExperiment` and `SingleCellExperiment` S4 classes. ***This is possible because of [Aaron's rds2cpp library](https://github.com/LTLA/rds2cpp).***

The package uses memory views (except for strings) to access the same memory from C++ in Python (through Cython of course). This is especially useful for large datasets so we don't make multiple copies of data.

## Install

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py
```

## Usage

If you do not have an RDS object handy, feel free to download from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

```python
from rds2py import as_SCE, read_rds

rObj = read_rds(<path_to_file>)
```

Once we have a realized structure of the RDS file, we can now build useful Python representations.

This `rObj` contains the realized structure of the RDS file as a Python `dict` object, it contains two keys 
- `data`: if atomic entities, contains the numpy view of the memory space.
- `attributes`: additional properties available for the object. 

The package provides friendly functions to easily convert few R representations to Python representations.

```python
from rds2py import as_spase_matrix, as_SCE

# to convert an robject to a sparse matrix
sp_mat = as_sparse(rObj)

# to convert an robject to SCE
sce = as_SCE(rObj)
```

For more use cases converting `data.frame`, `dgCMatrix`, `dgRMatrix` to Python, checkout the [documentation](https://biocpy.github.io/rds2py/).

***If you want to add more representations, feel free to send a PR on this repository!***


## Developer Notes

This project uses Cython to provide bindings from C++ to Python. It tries to use the same memory space (except for strings) instead of making copy of the data.

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

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
