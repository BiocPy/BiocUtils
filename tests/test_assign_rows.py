from biocutils import assign_rows
import numpy as np


def test_assign_numpy():
    y = np.random.rand(10, 20)
    y2 = np.random.rand(5, 20)
    expected = np.concatenate([y2, y[5:10,:]])
    assert (assign_rows(y, range(5), y2) == expected).all()

    # Same result with the default method.
    assert (assign_rows.registry[object](y, range(5), y2) == expected).all()
