# Tutorial: Getting Started with rds2py

Welcome to the `rds2py` tutorial! In this guide, we'll walk through how to read and write RDS and RData files in Python, parse objects into raw representations, and work with Python/BiocPy data structures.

---

## 1. Basic Reading

Reading an RDS file is designed to be a one-line operation. Under the hood, `rds2py` reads the data format and instantiates corresponding Python or Bioconductor classes (from the `BiocPy` ecosystem) where possible.

```python
from rds2py import read_rds, read_rda

# 1. Read a single R object from an RDS file
my_object = read_rds("path/to/file.rds")

# 2. Read all objects from an RData workspace file
# This returns a dictionary mapping variable names to their Python counterparts
workspace = read_rda("path/to/file.rda")
for name, obj in workspace.items():
    print(f"Loaded object: {name} of type {type(obj)}")
```

*Note: If you need an RDS file to experiment with, you can download some pre-made test files from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).*

---

## 2. Basic Writing (Saving)

You can write Python data structures back to R's native formats. `rds2py` automatically translates standard Python lists, NumPy arrays, SciPy sparse matrices, and BiocPy S4 objects into the correct representation formats.

```python
import numpy as np
from rds2py import write_rds, write_rda
from genomicranges import GenomicRanges
from iranges import IRanges

# 1. Save a NumPy array as an RDS integer vector
data_array = np.array([1, 2, 3, 4], dtype=np.int32)
write_rds(data_array, "vector.rds")

# 2. Save a Bioconductor GenomicRanges S4 object
gr = GenomicRanges(
    seqnames=["chr1", "chr2"],
    ranges=IRanges(start=[1, 100], width=[10, 50]),
    strand=["+", "-"]
)
write_rds(gr, "granges.rds")

# 3. Save multiple objects to an RData workspace file
workspace_objects = {
    "my_data": data_array,
    "my_ranges": gr
}
write_rda(workspace_objects, "workspace.rda")
```

---

## 3. Raw Dictionary Parsing (Custom Readers)

Sometimes you want to inspect the structure of an RDS file without automatically converting it to Python classes, or you might want to write a custom reader for an unsupported S4 class. 

For these scenarios, use `parse_rds` or `parse_rda`. They return the raw RDS tree structure as nested Python dictionaries:

```python
from rds2py import parse_rds
from rds2py.read_granges import read_genomic_ranges

# Parse the RDS file into a raw nested dictionary representation
raw_representation = parse_rds("path/to/file.rds")
print(raw_representation)

# If you know the underlying S4 class is a GRanges object, 
# you can use a parser directly:
if raw_representation.get("class_name") == "GRanges":
    gr = read_genomic_ranges(raw_representation)
    print(gr)
```

---

## Type Conversion Reference

The following table summarizes how basic R data structures map to Python, NumPy, and SciPy types:

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

### BiocPy Ecosystem Support
If optional dependencies are installed (`pip install rds2py[optional]`), R S4 classes are automatically converted:
- **GenomicRanges** / **GRanges** <-> `genomicranges.GenomicRanges`
- **GenomicRangesList** / **GRangesList** <-> `genomicranges.CompressedGenomicRangesList`
- **SummarizedExperiment** <-> `summarizedexperiment.SummarizedExperiment`
- **RangedSummarizedExperiment** <-> `summarizedexperiment.RangedSummarizedExperiment`
- **SingleCellExperiment** <-> `singlecellexperiment.SingleCellExperiment`
- **MultiAssayExperiment** <-> `multiassayexperiment.MultiAssayExperiment`
