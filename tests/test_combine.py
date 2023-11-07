import numpy as np
import pandas as pd
from biocutils import combine
from scipy import sparse as sp
import pytest

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_basic_list():
    x = [1, 2, "c"]
    y = ["a", "b"]

    z = combine(x, y)

    assert z == x + y
    assert isinstance(z, list)
    assert len(z) == len(x) + len(y)


def test_basic_mixed_dense_list():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])

    zcomb = combine(xd, y)

    z = x + y

    assert zcomb == z
    assert isinstance(zcomb, list)
    assert len(zcomb) == len(xd) + len(y)
