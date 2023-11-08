from biocutils import get_height
import numpy as np


def test_get_height():
    assert get_height([1,2,3]) == 3
    assert get_height(np.array([1,2,3])) == 3
    assert get_height(np.random.rand(10, 20)) == 10
