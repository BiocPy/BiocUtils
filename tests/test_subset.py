from biocutils import subset
import numpy as np


def test_subset_overall():
    x = [1, 2, 3, 4, 5]
    assert subset(x, [0, 2, 4]) == [1, 3, 5]

    y = np.random.rand(10, 20)
    assert (subset(y, range(5)) == y[0:5, :]).all()
