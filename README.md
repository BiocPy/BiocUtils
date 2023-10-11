<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/biocutils.svg?branch=main)](https://cirrus-ci.com/github/<USER>/biocutils)
[![ReadTheDocs](https://readthedocs.org/projects/biocutils/badge/?version=latest)](https://biocutils.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/biocutils/main.svg)](https://coveralls.io/r/<USER>/biocutils)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/biocutils.svg)](https://anaconda.org/conda-forge/biocutils)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/biocutils)
-->

# Utilities for BiocPy

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/biocutils.svg)](https://pypi.org/project/biocutils/)
[![Monthly Downloads](https://pepy.tech/badge/biocutils/month)](https://pepy.tech/project/biocutils)
![Unit tests](https://github.com/BiocPy/biocutils/actions/workflows/pypi-test.yml/badge.svg)

## Motivation

This repository contains a variety of simple utilities for the [BiocPy](https://github.com/BiocPy) project,
mostly convenient aspects of R that aren't provided by base Python.
The aim is to simplify development of higher-level packages like [**scranpy**](https://github.com/BiocPy/scranpy) and [**singler**](https://github.com/BiocPy/singler)
that would otherwise have to implement these methods individually.

## Available utilities

### `match`

```python
import biocutils
biocutils.match(["A", "C", "E"], ["A", "B", "C", "D", "E"])
## [0, 2, 4]
```

### `factor`

```python
import biocutils
biocutils.factor(["A", "B", "B", "A", "C", "D", "C", "D"])
## (['A', 'B', 'C', 'D'], [0, 1, 1, 0, 2, 3, 2, 3])
```

### `intersect`

```python
import biocutils
biocutils.intersect(["A", "B", "C", "D"], ["D", "A", "E"])
## ['A', 'D']
```

### `union`

```python
import biocutils
biocutils.union(["A", "B", "C", "D"], ["D", "A", "E"])
## ['A', 'B', 'C', 'D', 'E']
```

### `subset`

```python
import biocutils
biocutils.subset(["A", "B", "C", "D", "E"], [0, 2, 4])
## ['A', 'C', 'E']

import numpy as np
y = np.array([10, 20, 30, 40, 50])
biocutils.subset(y, [0, 2, 4])
## array([10, 30, 50])
```

### `is_list_of_type`

Checks if all elements of a list or tuple are of the same type.

```python
import biocutils
import numpy as np

x = [np.random.rand(3), np.random.rand(3, 2)]
biocutils.is_list_of_type(x, np.ndarray)
## True
```
