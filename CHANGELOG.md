# Changelog

## Version 0.3.0 - 0.3.4

- Provide a base `BiocObject` class similar to the `Annotated` class in Bioconductor. The class provides `metadata` slot, accessors and validation functions.
- Update Github actions and workflow to the new biocsetup versions
- Changes to improve `NamedList`, `Names` classes
  - get name at index
  - delete method for namedlist/names
  - add is_unique
  - add lint errors
- linting documentation, typehints etc

## Version 0.2.3

- Improve robustness of `show_as_cell()` to long strings, strings with newlines, and non-iterable objects.

## Version 0.2.2

- Fix `is_list_of_type()` so that they work correctly with NumPy's masked arrays.

## Version 0.2.1

- Added a `which()` function to get the indices of truthy values.

## Version 0.2.0

- chore: Remove Python 3.8 (EOL)
- precommit: Replace docformatter with ruff's formatter

## Version 0.1.7

- Added a `dtype=` option to `match()` to control the output array type.

## Version 0.0.1

- First release of the package.
