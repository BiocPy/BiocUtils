from biocutils import subset
import numpy as np


def test_subset_list():
    x = [1, 2, 3, 4, 5]
    assert subset(x, [0, 2, 4]) == [1, 3, 5]

    x = [1, 2, 3, 4, 5]
    assert subset(x, slice(None)) == x

    x = [1, 2, 3, 4, 5]
    assert subset(x, range(4, -1, -1)) == [5, 4, 3, 2, 1]


def test_subset_numpy():
    y = np.random.rand(10)
    assert (subset(y, slice(0, 5)) == y[0:5]).all()

    y = np.random.rand(10, 20)
    assert (subset(y, slice(0, 5)) == y[0:5, :]).all()
