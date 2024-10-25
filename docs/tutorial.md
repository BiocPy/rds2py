# Tutorial

If you do not have an RDS object handy, feel free to download one from [single-cell-test-files](https://github.com/jkanche/random-test-files/releases).

### Basic Usage

```python
from rds2py import read_rds
r_obj = read_rds("path/to/file.rds")
```

The returned `r_obj` either returns an appropriate Python class if a parser is already implemented or returns the dictionary containing the data from the RDS file.

## Write-your-own-reader

In addition, the package provides the dictionary representation of the RDS file, allowing users to write their own custom readers into appropriate Python representations.

```python
from rds2py import parse_rds

data = parse_rds("path/to/file.rds")
print(data)

# now write your own parser to convert this dictionary.
```

## Type Conversion Reference

| R Type | Python/NumPy Type |
|--------|------------------|
| numeric | numpy.ndarray (float64) |
| integer | numpy.ndarray (int32) |
| character | list of str |
| logical | numpy.ndarray (bool) |
| factor | list |
| data.frame | BiocFrame |
| matrix | numpy.ndarray or scipy.sparse matrix |
| dgCMatrix | scipy.sparse.csc_matrix |
| dgRMatrix | scipy.sparse.csr_matrix |

Check out the module reference for more information on these classes.
