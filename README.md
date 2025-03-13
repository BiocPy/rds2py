[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/rds2py.svg)](https://pypi.org/project/rds2py/)
![Unit tests](https://github.com/BiocPy/rds2py/actions/workflows/run-tests.yml/badge.svg)

# rds2py

Parse and construct Python representations for datasets stored in RDS files. `rds2py` supports various base classes from R, and Bioconductor's `SummarizedExperiment` and `SingleCellExperiment` S4 classes. **_For more details, check out [rds2cpp library](https://github.com/LTLA/rds2cpp)._**

---

**Version 0.5.0** brings major changes to the package,

- Complete overhaul of the codebase using pybind11
- Streamlined readers for R data types
- Updated API for all classes and methods

Please refer to the [documentation](https://biocpy.github.io/rds2py/) for the latest usage guidelines. Previous versions may have incompatible APIs.

---

The package provides:

- Efficient parsing of RDS files with _minimal_ memory overhead
- Support for R's basic data types and complex S4 objects
  - Vectors (numeric, character, logical)
  - Factors
  - Data frames
  - Matrices (dense and sparse)
  - Run-length encoded vectors (Rle)
- Conversion to appropriate Python/NumPy/SciPy data structures
  - dgCMatrix (sparse column matrix)
  - dgRMatrix (sparse row matrix)
  - dgTMatrix (sparse triplet matrix)
- Preservation of metadata and attributes from R objects
- Integration with BiocPy ecosystem for Bioconductor classes
  - SummarizedExperiment
  - RangedSummarizedExperiment
  - SingleCellExperiment
  - GenomicRanges
  - MultiAssayExperiment

## Installation

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py

# or install optional dependencies
pip install rds2py[optional]
```

By default, the package does not install packages to convert python representations to BiocPy classes. Please consider installing all optional dependencies.

## Usage

If you do not have an RDS object handy, feel free to download one from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

```python
from rds2py import read_rds
r_obj = read_rds("path/to/file.rds")
```

The returned `r_obj` either returns an appropriate Python class if a parser is already implemented or returns the dictionary containing the data from the RDS file.

In addition, the package provides the dictionary representation of the RDS file.

```python
from rds2py import parse_rds

robject_dict = parse_rds("path/to/file.rds")
print(robject_dict)
```

### Write-your-own-reader

Reading RDS files as dictionary representations allows users to write their own custom readers into appropriate Python representations.

```python
from rds2py import parse_rds

robject = parse_rds("path/to/file.rds")
print(robject)
```

if you know this RDS file contains an `GenomicRanges` object, you can use the built-in reader or write your own reader to convert this dictionary.

```python
from rds2py.read_granges import read_genomic_ranges

gr = read_genomic_ranges(robject)
print(gr)
```

## Type Conversion Reference

| R Type     | Python/NumPy Type                    |
| ---------- | ------------------------------------ |
| numeric    | numpy.ndarray (float64)              |
| integer    | numpy.ndarray (int32)                |
| character  | list of str                          |
| logical    | numpy.ndarray (bool)                 |
| factor     | list                                 |
| data.frame | BiocFrame                            |
| matrix     | numpy.ndarray or scipy.sparse matrix |
| dgCMatrix  | scipy.sparse.csc_matrix              |
| dgRMatrix  | scipy.sparse.csr_matrix              |

## Developer Notes

This project uses pybind11 to provide bindings to the rds2cpp library. Please make sure necessary C++ compiler is installed on your system.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
