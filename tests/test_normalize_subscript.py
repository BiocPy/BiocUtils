from biocutils import normalize_subscript, Names
import pytest
import numpy


def test_normalize_subscript_scalars():
    assert normalize_subscript(10, 100) == ([10], True)
    assert normalize_subscript(-1, 100) == ([99], True)
    assert normalize_subscript(True, 100) == ([0], True)
    assert normalize_subscript(False, 100) == ([], False)
    assert normalize_subscript("C", 5, ["A", "B", "C", "D", "E"]) == ([2], True)
    assert normalize_subscript("B", 5, ["A", "B", "C", "B", "E"]) == (
        [1],
        True,
    )  # takes first occurence.

    with pytest.raises(IndexError) as ex:
        normalize_subscript(100, 10)
    assert str(ex.value).find("subscript (100)") >= 0

    with pytest.raises(IndexError) as ex:
        normalize_subscript(-11, 10)
    assert str(ex.value).find("subscript (-11)") >= 0

    with pytest.raises(IndexError) as ex:
        normalize_subscript("foor", 10)
    assert str(ex.value).find("subscript 'foor'") >= 0

    with pytest.raises(ValueError) as ex:
        normalize_subscript("F", 5, ["A", "B", "C", "D", "E"])


def test_normalize_subscript_slice():
    assert normalize_subscript(slice(10, 40), 100) == (range(10, 40), False)
    assert normalize_subscript(slice(-10, -20, -1), 100) == (range(90, 80, -1), False)


def test_normalize_subscript_range():
    assert normalize_subscript(range(5, 2), 100) == ([], False)
    assert normalize_subscript(range(10, 40), 100) == (range(10, 40), False)
    assert normalize_subscript(range(-10, 40), 100) == (
        list(range(90, 100)) + list(range(40)),
        False,
    )
    assert normalize_subscript(range(50, -10, -1), 100) == (
        list(range(50, -1, -1)) + list(range(99, 90, -1)),
        False,
    )
    assert normalize_subscript(range(-10, -50, -1), 100) == (range(90, 50, -1), False)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(range(10, 50), 20)
    assert str(ex.value).find("subscript (49)") >= 0
    normalize_subscript(range(10, 20), 20)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(range(20, 0, -1), 20)
    assert str(ex.value).find("subscript (20)") >= 0
    normalize_subscript(range(19, 0, -1), 20)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(range(-21, -10), 20)
    assert str(ex.value).find("subscript (-21)") >= 0
    normalize_subscript(range(-20, -10), 20)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(range(-10, -22, -1), 20)
    assert str(ex.value).find("subscript (-21)") >= 0
    normalize_subscript(range(-10, -21, -1), 20)


def test_normalize_subscript_chaos():
    assert normalize_subscript([0, 2, 4, 6, 8], 50) == ([0, 2, 4, 6, 8], False)

    with pytest.raises(IndexError) as ex:
        normalize_subscript([0, 2, 50, 6, 8], 50)
    assert str(ex.value).find("subscript (50)") >= 0

    assert normalize_subscript([0, -1, 2, -3, 4, -5, 6, -7, 8], 50) == (
        [0, 49, 2, 47, 4, 45, 6, 43, 8],
        False,
    )

    with pytest.raises(IndexError) as ex:
        normalize_subscript([0, 2, -51, 6, 8], 50)
    assert str(ex.value).find("subscript (-51)") >= 0

    assert normalize_subscript([False, 10, True, 20, False, 30, True], 50) == (
        [10, 2, 20, 30, 6],
        False,
    )

    names = ["A", "B", "C", "D", "E", "F"]
    assert normalize_subscript(["B", 1, "D", 2, "F", 3, "A"], 6, names) == (
        [1, 1, 3, 2, 5, 3, 0],
        False,
    )
    assert normalize_subscript(["B", 1, "D", 2, "F", 3, "A"], 6, Names(names)) == (
        [1, 1, 3, 2, 5, 3, 0],
        False,
    )
    assert normalize_subscript(
        ["B", 1, "A", 2, "B", 3, "A"], 6, ["A", "B", "A", "B", "A", "B"]
    ) == (
        [1, 1, 0, 2, 1, 3, 0],
        False,
    )  # Takes the first occurence.

    with pytest.raises(KeyError) as ex:
        normalize_subscript(["B", 1, "D", 2, "G", 3, "A"], 6, names)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(["B", 1, "D", 2, "F", 3, "A"], 6)
    assert str(ex.value).find("vector-like object with no names") >= 0


def test_normalize_subscript_numpy():
    out, x = normalize_subscript(numpy.array([1, 3, 5]), 6)
    assert (out == numpy.array([1, 3, 5])).all()

    out, x = normalize_subscript(numpy.array([-1, -3, -5]), 6)
    assert (out == numpy.array([5, 3, 1])).all()

    assert normalize_subscript(numpy.int64(5), 6) == ([5], True)
    assert normalize_subscript(numpy.bool_(True), 6) == ([0], True)

    # Now the trickiest part - are booleans converted correctly?
    assert normalize_subscript(numpy.array([True, False, True, False, True]), 5) == (
        [0, 2, 4],
        False,
    )


def test_normalize_subscript_allow_negative():
    assert normalize_subscript(-50, 100, non_negative_only=False) == ([-50], True)
    assert normalize_subscript(range(50, -10, -1), 100, non_negative_only=False) == (
        range(50, -10, -1),
        False,
    )
    assert normalize_subscript(range(-10, -50, -1), 100, non_negative_only=False) == (
        range(-10, -50, -1),
        False,
    )
    assert normalize_subscript(
        [0, -1, 2, -3, 4, -5, 6, -7, 8], 50, non_negative_only=False
    ) == ([0, -1, 2, -3, 4, -5, 6, -7, 8], False)

    with pytest.raises(IndexError) as ex:
        normalize_subscript(
            [0, -1, 2, -3, 4, -51, 6, -7, 8], 50, non_negative_only=False
        )
    assert str(ex.value).find("subscript (-51) out of range") >= 0
