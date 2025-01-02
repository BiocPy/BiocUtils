import biocutils
import numpy


def test_which_list():
    out = biocutils.which([True, False, False, True])
    assert (out == numpy.array([0, 3])).all()

    y = [False] * 10000
    idx = sorted(list(set((numpy.random.rand(1000) * 10000).astype(numpy.int32))))
    for i in idx:
        y[i] = True

    out = biocutils.which(y)
    assert (out == numpy.array(idx)).all()


def test_which_numpy():
    x = numpy.array([1, 0, 5, -1, 0, 0])

    out = biocutils.which(x)
    assert (out == numpy.array([0, 2, 3])).all()

    out = biocutils.which(x, dtype=numpy.uint32)
    assert out.dtype == numpy.uint32
