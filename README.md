[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/rds2py.svg)](https://pypi.org/project/rds2py/)
![Unit tests](https://github.com/BiocPy/rds2py/actions/workflows/run-tests.yml/badge.svg)

# rds2py

Parse and construct Python representations for datasets stored in **RDS or RData** files. `rds2py` supports various base classes from R, and Bioconductor's `SummarizedExperiment` and `SingleCellExperiment` S4 classes. **_For more details, check out [rds2cpp library](https://github.com/LTLA/rds2cpp)._**

## Fixes
Cloned from [rds2py](https://github.com/BiocPy/rds2py). The repo can't be installed on Windows. With a AI agent, a few fixes are made to make it installable on Windows. Here's a summary of the four issues that were fixed:

1. lib/src/rdswrapper.cpp — Updated for new rds2cpp API
The upstream rds2cpp library had breaking API changes:
Attributes: Changed from a struct with .names/.values vectors to std::vector<Attribute> where each Attribute has a SymbolIndex name + unique_ptr<RObject> value. Attribute names now require a lookup into a global symbols table.
StringVector::data: Changed from vector<string> to vector<String> where String has an optional<string> value (supports missing/NA strings).
RdaFile: contents (a PairList-like struct with .tag_names, .has_tag, .data) was replaced by objects (a vector<RdaObject> with .name as SymbolIndex and .value).
The RdsReader class now carries a const std::vector<rds2cpp::Symbol>* pointer to resolve symbol names. Added #include <algorithm>.

2. lib/CMakeLists.txt — Added zlib for Windows
The byteme library conditionally includes gzip support only when zlib.h is available (#if __has_include("zlib.h")). On Windows, zlib isn't typically installed. Added CMake logic to auto-fetch and build zlib from source via FetchContent when the system zlib isn't found.

3. setup.py — Fixed Windows file copy
The old code copied _core.dll → _core.pyd, but the actual CMake output is named lib_rds_parser.
pybind11 appends ABI tags (e.g. lib_rds_parser.cp312-win_amd64.pyd), so a glob pattern is now used to find the built file.
4. setup.cfg — Added Windows platform
Changed platforms = Mac, Linux to platforms = Mac, Linux, Windows.


## Installation

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py

# or install optional dependencies
pip install rds2py[optional]
```

By default, the package does not install packages to convert python representations to BiocPy classes. Please consider installing all optional dependencies.

## Usage

> [!NOTE]
>
> If you do not have an RDS object handy, feel free to download one from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

```python
from rds2py import read_rds, read_rda
r_obj = read_rds("path/to/file.rds") # or read_rda("path/to/file.rda")
```

The returned `r_obj` either returns an appropriate Python class if a parser is already implemented or returns the dictionary containing the data from the RDS file.

### Write-your-own-reader

Reading RDS or RData files as dictionary representations allows users to write their own custom readers into appropriate Python representations.

```python
from rds2py import parse_rds, parse_rda

robject = parse_rds("path/to/file.rds") # or use parse_rda for rdata files
print(robject)
```

If you know this RDS file contains an `GenomicRanges` object, you can use the built-in reader or write your own reader to convert this dictionary.

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

and integration with BiocPy ecosystem for Bioconductor classes
  - SummarizedExperiment
  - RangedSummarizedExperiment
  - SingleCellExperiment
  - GenomicRanges
  - MultiAssayExperiment

## Developer Notes

This project uses pybind11 to provide bindings to the rds2cpp library. Please make sure necessary C++ compiler is installed on your system.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
