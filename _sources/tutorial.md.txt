# Tutorial

If you do not have an RDS object handy, feel free to download from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

## Step 1: Read a RDS file in Python

The first step is to read an RDS file and get the equivalent representation in Python.

```python
from rds2py import read_rds

rObj = read_rds(<path_to_file>)
```

Once we have a realized structure of the RDS file, we can now start to build useful Python representations.

This `rObj` contains the realized structure of the RDS file as a Python `dict` object, it contains two keys 
- `data`: if atomic entities, contains the numpy view of the memory space.
- `attributes`: additional properties available for the object. 

The package provides friendly functions to convert some R representations to useful Python representations.

## Step 2: Python representations

### Matrices

Use these methods if the RDS file contains either a sparse matrix (`dgCMatrix` or `dgRMatrix`) or a dense matrix.


***Note: If an R object contains `dims` in the `attributes`, we consider this as a matrix.***

```python
from rds2py import as_spase_matrix, as_dense_matrix

# to convert an robject to a sparse matrix
sp_mat = as_sparse_matrix(rObj)

# to convert an robject to a sparse matrix
dense_mat = as_dense_matrix(rObj)
```

### Pandas DataFrame

Methods are available to construct a pandas `DataFrame` from data stored in an RDS file. The package supports two R classes for this operation - `data.frame` and `DFrame` classes.

```python
from rds2py import as_pandas

# to convert an robject to DF
df = as_pandas(rObj)
```

### S4 classes: specifically `SingleCellExperiment` or `SummarizedExperiment`

We also support `SingleCellExperiment` or `SummarizedExperiment` from Bioconductor. the `as_SCE` method is how we one can do this operation. 

***Note: This method also serves as an example on how to convert complex R structures into Python representations.***

```python
from rds2py import as_SCE

# to convert an robject to SCE
sp_mat = as_SCE(rObj)
```

Well thats it, hack on & create more base representations to encapsulate complex structures. If you want to add more representations, feel free to send a PR on this repository!