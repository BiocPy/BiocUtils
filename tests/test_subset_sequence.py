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


def test_subset_range():
    x = range(10, 20)
    assert subset_sequence(x, range(2, 8, 2)) == range(12, 18, 2)
    assert subset_sequence(x, [0, 1, 5, 9]) == [10, 11, 15, 19]
    assert subset_sequence(x, range(9, -1, -1)) == range(19, 9, -1)

    x = range(10, 30, 3)
    assert subset_sequence(x, range(2, 7, 2)) == x[2:7:2]
    assert subset_sequence(x, range(5, 0, -2)) == x[5:0:-2]
    assert subset_sequence(x, range(len(x) - 1, -1, -1)) == x[::-1]

    x = range(100, 21, -6)
    assert subset_sequence(x, range(3, 10, 2)) == x[3:10:2]
    assert subset_sequence(x, range(7, 1, -1)) == x[7:1:-1]
    assert subset_sequence(x, range(len(x) - 1, -1, -1)) == x[::-1]
