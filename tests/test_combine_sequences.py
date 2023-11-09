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
    xd = np.array(x)
    yd = np.array(y)

    zcomb = combine_sequences(xd, yd)
    z = x + y
    zd = np.array(z)
    assert (zcomb == zd).all()


def test_basic_dense_masked():
    x = [1, 2, 3]
    y = [0.1, 0.2]
    xd = np.array(x)
    yd = np.ma.array(y, mask=[True]*2) 

    zcomb = combine_sequences(xd, yd)
    z = x + y
    zd = np.ma.array(z, mask=[False]*3 + [True]*2)
    assert (zcomb == zd).all()
    assert (zcomb.mask == zd.mask).all()


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


def test_ranges():
    assert combine_sequences(range(0, 10), range(10, 54)) == range(0, 54)
    assert combine_sequences(range(2, 5), range(5, 9), range(9, 20)) == range(2, 20)
    assert combine_sequences(range(2, 9, 2), range(10, 54, 2)) == range(2, 54, 2)
    assert combine_sequences(range(10, 5, -1), range(5, -1, -1)) == range(10, -1, -1)

    # Trigger a fallback.
    assert combine_sequences(range(0, 10), [10, 11, 12, 13]) == list(range(0, 14))
    assert combine_sequences(range(0, 10), range(20, 54)) == list(range(0, 10)) + list(range(20, 54))

    # Empty ranges are handled correctly.
    assert combine_sequences(range(10, 10), range(50, 50), range(20, 20)) == range(10, 10)
    assert combine_sequences(range(0, 10), range(50, 50), range(10, 20)) == range(0, 20)

    # Different steps trigger a fallback, unless it's of length 1.
    assert combine_sequences(range(0, 10), range(10, 50, 2)) == list(range(0, 10)) + list(range(10, 50, 2))
    assert combine_sequences(range(0, 10), range(10, 11, 5), range(11, 19)) == range(0, 19)
