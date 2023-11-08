from biocutils import is_high_dimensional
import numpy


def test_is_high_dimensional():
    assert not is_high_dimensional([1,2,3])
    assert not is_high_dimensional(numpy.array([1,2,3]))
    assert is_high_dimensional(numpy.random.rand(10, 20, 30))
