# Tutorial

If you do not have an RDS object handy, feel free to download from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

## Step 1: Read a RDS file into Python

The first step is to read an RDS file and get the equivalent representation in Python.

```python
from rds2py import as_SCE, read_rds

rObj = read_rds(<path_to_file>)
```

Once we have a realized structure of the RDS file, we can now start to build useful Python representations. We provide a few common methods to easily convert a realized R object. 

## Step 2: Python representations

### Matrices

if the Rds file holds either a sparse matrix (`dgCMatrix` or `dgRMatrix`) or a dense matrix.


***Note: Currently, if an R object contains `dims` in the `attributes`, we consider this as a matrix.***

```python
from rds2py import as_spase_matrix, as_dense_matrix

# to convert an robject to a sparse matrix
sp_mat = as_sparse_matrix(rObj)

# to convert an robject to a sparse matrix
dense_mat = as_dense_matrix(rObj)
```

### Dataframes

Similarly methods are available to create a pandas `DataFrame`. The package supports two main R classes for this operation - the base `data.frame` representation and `DFrame`.

```python
from rds2py import as_pandas_from_data_frame, as_pandas_from_dframe,

# to convert an robject to DF
df = as_pandas_from_data_frame(rObj)
```

### Bioconductor `SingleCellExperiment` or `SummarizedExperiment`

We also support SCE or SE from Bioconductor. the `as_SCE` method is how we one can do this operation. 

This method also serves as a example on how to convert complicated structures to useful representations. 

```python
from rds2py import as_spase_matrix, as_dense_matrix

# to convert an robject to SCE
sp_mat = as_SCE(rObj)
```

Well thats it, hack on, create more base representations to encapsulate complex structures.

feel free to send me a PR!