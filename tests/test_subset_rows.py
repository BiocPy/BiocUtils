from biocutils import subset_rows
import numpy as np


def test_subset_numpy():
    y = np.random.rand(10)
    assert (subset_rows(y, range(5)) == y[0:5]).all()

    y = np.random.rand(10, 20)
    assert (subset_rows(y, range(5)) == y[0:5, :]).all()

    y = np.random.rand(10, 20, 30)
    assert (subset_rows(y, range(5)) == y[0:5, :, :]).all()
