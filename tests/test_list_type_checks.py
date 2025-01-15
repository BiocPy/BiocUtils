import numpy as np
import numpy.ma as ma
import pytest
from biocutils import is_list_of_type


def test_simple_list():
    x = [1, 2, 3]

    assert is_list_of_type(x, int)

    y = [1.2, 2.3, 4.5]
    assert is_list_of_type(y, float)

    xt = (1, 2, 3)
    assert is_list_of_type(xt, int)

    xt = (1, 2, None)
    assert not is_list_of_type(xt, int)
    assert is_list_of_type(xt, int, ignore_none=True)


def test_should_fail():
    x = [1, [2, 3, 4], 6]

    assert is_list_of_type(x, int) is False


def test_numpy_elems():
    x = [np.random.rand(3), np.random.rand(3, 2)]

    assert is_list_of_type(x, np.ndarray)

def test_numpy_arrays():
    x = np.random.rand(3)

    assert is_list_of_type(x, float)

    x = ma.array([1, None, 3], mask = [0, 1, 0], dtype=np.float32)

    assert is_list_of_type(x, np.float32, ignore_none=True)
    assert is_list_of_type(x, np.float32) is False
