from biocutils import subset_sequence
import numpy as np


def test_subset_list():
    x = [1, 2, 3, 4, 5]
    assert subset_sequence(x, [0, 2, 4]) == [1, 3, 5]

    x = [1, 2, 3, 4, 5]
    assert subset_sequence(x, range(5)) == x

    x = [1, 2, 3, 4, 5]
    assert subset_sequence(x, range(4, -1, -1)) == [5, 4, 3, 2, 1]


def test_subset_numpy():
    y = np.random.rand(10)
    assert (subset_sequence(y, range(5)) == y[0:5]).all()

    y = np.random.rand(10, 20)
    assert (subset_sequence(y, range(5)) == y[0:5, :]).all()
