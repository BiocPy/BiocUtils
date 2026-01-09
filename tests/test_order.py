import biocutils
import numpy


def test_order_simple():
    o = biocutils.order(["D", "B", "C", "A"])
    assert list(o) == [3, 1, 2, 0]
    assert o.dtype == numpy.dtype("uint8")

    o = biocutils.order(["D", "B", "C", "A"], dtype=numpy.dtype("uint32"))
    assert list(o) == [3, 1, 2, 0]
    assert o.dtype == numpy.dtype("uint32")

    # Handles ties stably.
    o = biocutils.order(["D", "B", "D", "C", "A", "D"])
    assert list(o) == [4, 1, 3, 0, 2, 5]

    # Reverses correctly with stable ties.
    o = biocutils.order(["D", "B", "D", "C", "A", "D"], decreasing=True)
    assert list(o) == [0, 2, 5, 3, 1, 4]

    # Ignores incomparable values.
    o = biocutils.order(["D", "B", None, "C", "A"])
    assert list(o) == [4, 1, 3, 0, 2]

    o = biocutils.order(["D", "B", "C", "A"], force_last=[]) # for coverage purposes.
    assert list(o) == [3, 1, 2, 0]


def test_order_Factor():
    f = biocutils.Factor.from_sequence(["D", "B", "C", "A"])
    o = biocutils.order(f)
    assert list(o) == [3, 1, 2, 0]
    o = biocutils.order(f, decreasing=True)
    assert list(o) == [0, 2, 1, 3]

    o = biocutils.order(f, force_last=[]) # for coverage purposes.
    assert list(o) == [3, 1, 2, 0]

    # Respects the level ordering.
    o = biocutils.order(biocutils.Factor.from_sequence(["D", "B", "C", "A"], ["D", "C", "B", "A"]))
    assert list(o) == [0, 2, 1, 3]

    # Respects various incomparable values.
    f = biocutils.Factor.from_sequence(["D", "B", None, "C", "A"])
    o = biocutils.order(f)
    assert list(o) == [4, 1, 3, 0, 2]
    o = biocutils.order(f, force_last=[None, "A"])
    assert list(o) == [1, 3, 0, 2, 4]


def test_order_sort():
    assert biocutils.sort(["A", "B", None, "C", "D"], decreasing=True) == ["D", "C", "B", "A", None]

    x = numpy.random.rand(20)
    s = biocutils.sort(x)
    assert s.dtype == x.dtype
    assert (s == sorted(x)).all()
