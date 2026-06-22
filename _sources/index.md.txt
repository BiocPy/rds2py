# rds2py: R Serialization Formats in Python

`rds2py` is designed to parse, extract, and write R data formats (RDS and RData) directly in Python. It provides native, out-of-the-box integration with the [BiocPy](https://github.com/biocpy) ecosystem, allowing seamless roundtripping of complex S4 datasets like `SummarizedExperiment`, `SingleCellExperiment`, and `GenomicRanges`.

This library is built on top of [Aaron Lun's rds2cpp library](https://github.com/LTLA/rds2cpp).

## Installation

`rds2py` is available on [PyPI](https://pypi.org/project/rds2py/):

```shell
pip install rds2py
```

To enable full conversion support for Bioconductor/BiocPy classes, consider installing the optional dependencies:

```shell
pip install rds2py[optional]
```

## Table of Contents

```{toctree}
:maxdepth: 2

Overview <readme>
Tutorial <tutorial>
Custom Serialization Guide <custom_serialization>
Contributions & Help <contributing>
License <license>
Authors <authors>
Changelog <changelog>
Module Reference <api/modules>
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

[Sphinx]: http://www.sphinx-doc.org/
[Markdown]: https://daringfireball.net/projects/markdown/
[reStructuredText]: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
[MyST]: https://myst-parser.readthedocs.io/en/latest/
