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
    xd = np.array(x)
    zcomb = combine(xd, y)

    z = x + y
    assert (zcomb == z).all()
    assert len(zcomb) == len(xd) + len(y)


def test_basic_mixed_dense_array():
    x = np.array([1, 2, 3, 4]).reshape((2,2))
    y = np.array([4, 5, 6, 7]).reshape((2,2))
    zcomb = combine(x, y)
    assert zcomb.shape == (4, 2)

    with pytest.raises(ValueError) as ex:
        combine(x, [1,2,3,4])
    assert str(ex.value).find("cannot mix") >= 0
