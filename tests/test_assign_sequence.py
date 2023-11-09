from biocutils import assign_sequence
import numpy as np


def test_assign_list():
    x = [1, 2, 3, 4, 5]
    assert assign_sequence(x, [2,3,4], [0, 2, 4]) == [1, 2, 0, 2, 4]

    # Same result with the default method.
    assert assign_sequence.registry[object](x, [1,3], ["A", "B"]) == [1, "A", 3, "B", 5]


def test_assign_numpy():
    y1 = np.random.rand(10)
    y2 = np.random.rand(5)
    expected = np.concatenate([y1[:5], y2])
    assert (assign_sequence(y1, range(5, 10), y2) == expected).all()


def test_assign_range():
    x = range(10, 20)
    assert assign_sequence(x, range(2, 7), ["A", "B", "C", "D", "E"]) == [10, 11, "A", "B", "C", "D", "E", 17, 18, 19]
    assert assign_sequence(x, range(2, 7), range(12, 17)) == range(10, 20)
