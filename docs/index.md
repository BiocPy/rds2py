# rds2py

Parse, extract and create Python representations for datasets stored in RDS files. It supports Bioconductor's `SummarizedExperiment` and `SingleCellExperiment` objects. This is possible because of [Aaron's rds2cpp library](https://github.com/LTLA/rds2cpp).

The package uses memory views (except for strings) so that we can access the same memory from C++ space in Python (through Cython of course). This is especially useful for large datasets so we don't make copies of data.

## Install

Package is published to [PyPI](https://pypi.org/project/rds2py/)

```shell
pip install rds2py
```

## Contents

```{toctree}
:maxdepth: 2

Overview <readme>
Tutorial <tutorial>
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
