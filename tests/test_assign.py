from biocutils import assign, assign_rows
import numpy as np


def test_assign_overall():
    x = [1, 2, 3, 4, 5]
    assert assign(x, [0, 2, 4], ["A", "B", "C"]) == ["A", 2, "B", 4, "C"]

    y = np.random.rand(10, 20)
    y2 = np.random.rand(5, 20)
    assert (assign(y, range(5), y2) == assign_rows(y, range(5), y2)).all()
