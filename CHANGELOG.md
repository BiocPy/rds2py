# Changelog

## Version 0.5.0

- Complete overhaul of the codebase using pybind11
- Streamlined readers for R data types
- Updated API for all classes and methods
- Updated documentation and tests.

## Version 0.4.5

- Switch to pybind11 to implementing the bindings to rds2cpp.
- Update tests, documentation and actions.
- Fix github issue with showing incorrect package version on github pages.

## Version 0.4.4

- Add methods to parse RDS files containing `GenomicRangesList`
- Fix bug in reading strand information; mostly RLE vectors.
- Update tests and documentation

## Version 0.4.0 - 0.4.3

- Migrate to the new class implementations
- Add reader for objects containing genomic ranges

## Version 0.3.0

This release migrates the package to a more palatable Google's Python style guide. A major modification to the package is with casing, all `camelCase` properties, methods, functions and parameters are now `snake_case`.

In addition, docstrings and documentation has been updated to use sphinx's features of linking objects to their types. Sphinx now also documents private and special dunder methods (e.g. `__getitem__`, `__copy__` etc). Intersphinx has been updated to link to references from dependent packages.

Configuration for flake8, ruff and black has been added to pyproject.toml and setup.cfg to be less annoying.

Finally, pyscaffold has been updated to use "myst-parser" as the markdown compiler instead of recommonmark. As part of the pyscaffold setup, one may use pre-commits to run some of the routine tasks of linting and formatting before every commit. While this is sometimes annoying and can be ignored with `--no-verify`, it brings some consistency to the code base.

## Version 0.1

- First implementation
