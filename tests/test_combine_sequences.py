import numpy as np
import pandas as pd
from biocutils import combine_sequences
from scipy import sparse as sp

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_basic_list():
    x = [1, 2, "c"]
    y = ["a", "b"]

    z = combine_sequences(x, y)

    assert z == x + y
    assert isinstance(z, list)
    assert len(z) == len(x) + len(y)


def test_basic_dense():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])
    yd = np.array([0.1, 0.2], dtype=float)

    zcomb = combine_sequences(xd, yd)

    z = x + y
    zd = np.array(z)

    assert all(np.isclose(zcomb, zd)) is True
    assert isinstance(zcomb, np.ndarray)
    assert len(zcomb) == len(zd)


def test_basic_mixed_dense_list():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array([1, 2, 3])

    zcomb = combine_sequences(xd, y)

    z = x + y
    assert (zcomb == z).all()
    assert len(zcomb) == len(xd) + len(y)


def test_basic_mixed_tuple_list():
    x = [1, 2, 3]
    y = (0.1, 0.2)
    xd = np.array([1, 2, 3])

    zcomb = combine_sequences(xd, y, x)

    z = x + list(y) + x
    assert (zcomb == z).all()
    assert len(zcomb) == 2 * len(xd) + len(y)


def test_pandas_series():
    s1 = pd.Series(["a", "b"])
    s2 = pd.Series(["c", "d"])

    z = combine_sequences(s1, s2)

    assert isinstance(z, pd.Series)
    assert len(z) == 4

    x = ["gg", "ff"]

    z = combine_sequences(s1, x)
    assert isinstance(z, pd.Series)
    assert len(z) == 4
