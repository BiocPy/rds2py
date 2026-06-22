[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/rds2py.svg)](https://pypi.org/project/rds2py/)
![Unit tests](https://github.com/BiocPy/rds2py/actions/workflows/run-tests.yml/badge.svg)

# rds2py

`rds2py` allows you to read and write R's native **RDS** and **RData** files directly in Python. Beyond standard R types, it provides integration with the [BiocPy](https://github.com/biocpy) ecosystem, allowing you to easily roundtrip complex S4 data structures like `SummarizedExperiment`, `SingleCellExperiment`, and `GenomicRanges`. **_For more details, check out [rds2cpp library](https://github.com/LTLA/rds2cpp)._**

## Installation

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py
```

To enable automatic conversion to Bioconductor/BiocPy classes, make sure to install the optional dependencies:

```shell
pip install rds2py[optional]
```


## Quickstart

### 1. Reading RDS and RData files

Reading an RDS or RData file is as simple as a single function call. `rds2py` automatically detects and maps known R/Bioconductor classes to their Python equivalents:

```python
from rds2py import read_rds, read_rda

# Read an RDS file (returns a Python/BiocPy object or dict)
data = read_rds("path/to/file.rds")

# Read objects from an RData workspace file (returns a dictionary of objects)
workspace = read_rda("path/to/workspace.rda")
```

If `rds2py` encounters an S4 class or complex R structure it doesn't have a parser registered for, it falls back to returning a dictionary so you don't lose any data.

### 2. Saving to RDS and RData files

You can serialize Python objects back to RDS or RData formats. This includes NumPy arrays, SciPy sparse matrices, standard dictionaries/lists, and BiocPy objects:

```python
import numpy as np
from rds2py import write_rds, write_rda
from genomicranges import GenomicRanges
from iranges import IRanges

# 1. Write an atomic NumPy array
write_rds(np.array([10, 20, 30], dtype=np.int32), "array.rds")

# 2. Write a complex Bioconductor GenomicRanges object
gr = GenomicRanges(seqnames=["chr1", "chr2"], ranges=IRanges(start=[1, 100], width=[10, 50]), strand=["+", "-"])
write_rds(gr, "genomic_ranges.rds")

# 3. Write multiple Python objects into a single RData workspace
objects = {"my_array": np.array([1.1, 2.2, 3.3]), "my_granges": gr}
write_rda(objects, "workspace.rda")
```

### 3. Custom Extensions

If you have custom S4 representations or class mapping needs, you can parse the raw RDS structure into Python dictionary representations using `parse_rds`/`parse_rda` and apply your custom deserializers:

```python
from rds2py import parse_rds
from rds2py.read_granges import read_genomic_ranges

# 1. Parse into a raw dictionary representation of the RDS tree
raw_dict = parse_rds("path/to/file.rds")
print(raw_dict.keys())  # ['type', 'class_name', 'attributes', 'data', ...]

# 2. Build or invoke custom parser logic
if raw_dict.get("class_name") == "GRanges":
    gr = read_genomic_ranges(raw_dict)
    print(gr)
```

For writing custom objects, you can register your classes to `rds2py`'s serialization registry using the `save_rds` singledispatch generic:

```python
from rds2py.generics import save_rds


class MyCustomClass:
    def __init__(self, value):
        self.value = value


@save_rds.register(MyCustomClass)
def _serialize_custom(x: MyCustomClass, path=None):
    # Construct the raw RDS dictionary representation expected by rds2cpp
    converted = {
        "type": "integer",
        "data": [x.value],
        "attributes": {"class": {"type": "string", "data": ["MyCustomRClass"]}},
    }

    # Optionally save if path is provided, otherwise return representation
    if path is not None:
        from rds2py.lib_rds_parser import write_rds as write_rds_native

        write_rds_native(converted, path)
    return converted
```


## Type Conversion Reference

The table below describes how core R types are mapped to Python/NumPy/SciPy counterparts:

| R Type / Class | Python / NumPy / SciPy Counterpart |
| :--- | :--- |
| **numeric** | `numpy.ndarray` (`float64`) |
| **integer** | `numpy.ndarray` (`int32`) |
| **logical** | `numpy.ndarray` (`bool`) |
| **character** | `list` of `str` |
| **factor** | `list` / representation levels |
| **matrix (dense)** | `numpy.ndarray` |
| **dgCMatrix** (Column-sparse) | `scipy.sparse.csc_matrix` |
| **dgRMatrix** (Row-sparse) | `scipy.sparse.csr_matrix` |
| **data.frame** / **DFrame** | `biocframe.BiocFrame` |

### Supported Bioconductor Classes
When `rds2py[optional]` is installed, the package fully translates R/S4 classes to their BiocPy equivalents:
- **GenomicRanges** / **GRanges** <-> `genomicranges.GenomicRanges`
- **GenomicRangesList** / **GRangesList** <-> `genomicranges.CompressedGenomicRangesList`
- **SummarizedExperiment** <-> `summarizedexperiment.SummarizedExperiment`
- **RangedSummarizedExperiment** <-> `summarizedexperiment.RangedSummarizedExperiment`
- **SingleCellExperiment** <-> `singlecellexperiment.SingleCellExperiment`
- **MultiAssayExperiment** <-> `multiassayexperiment.MultiAssayExperiment`

---

## Developer Notes

- `rds2py` uses `pybind11` to bind the core C++ `rds2cpp` library. Compiling from source requires a compatible C++ compiler.
- Tests can be run via `tox` or directly using `pytest`.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
