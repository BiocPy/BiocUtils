from biocutils import match, Factor
import numpy
import pytest


def test_match_simple():
    x = ["A", "C", "B", "D", "A", "A", "C", "D", "B"]
    levels = ["D", "C", "B", "A"]

    mm = match(x, levels)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    assert mm.dtype == numpy.dtype("int8")

    mm = match(x, levels, fail_missing=True, dtype=numpy.uint32)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    assert mm.dtype == numpy.dtype("uint32")


def test_match_duplicates():
    x = [5, 1, 2, 3, 5, 6, 7, 7, 2, 1]
    levels = [1, 2, 3, 3, 5, 6, 1, 7, 6]

    mm = match(x, levels)
    assert list(mm) == [4, 0, 1, 2, 4, 5, 7, 7, 1, 0]

    mm = match(x, levels, duplicate_method="last")
    assert list(mm) == [4, 6, 1, 3, 4, 8, 7, 7, 1, 6]


def test_match_none():
    x = ["A", None, "B", "D", None, "A", "C", None, "B"]
    mm = match(x, ["D", "C", "B", "A"])
    assert list(mm) == [3, -1, 2, 0, -1, 3, 1, -1, 2]

    lev = ["D", None, "C", "B", "A"]
    mm = match(x, lev)
    assert list(mm) == [4, 1, 3, 0, 1, 4, 2, 1, 3]

    mm = match(x, lev, incomparables=set([None]))
    assert list(mm) == [4, -1, 3, 0, -1, 4, 2, -1, 3]

    with pytest.raises(match="cannot find"):
        match(x, lev, incomparables=set([None]), fail_missing=True)


def test_match_dtype():
    levels = ["D", "C", "B", "A"]

    mm = match(["A", "F", "B", "D", "F", "A", "C", "F", "B"], levels, dtype=numpy.dtype("int32"))
    assert list(mm) == [3, -1, 2, 0, -1, 3, 1, -1, 2]
    assert mm.dtype == numpy.dtype("int32")

    mm = match(["A", "B", "D", "A", "C", "B"], levels, dtype=numpy.dtype("uint32"))
    assert list(mm) == [3, 2, 0, 3, 1, 2]
    assert mm.dtype == numpy.dtype("uint32")


def test_match_fail_missing():
    x = ["A", "E", "B", "D", "E"]
    levels = ["D", "C", "B", "A"]
    mm = match(x, levels)
    assert list(mm) == [3, -1, 2, 0, -1]

    with pytest.raises(ValueError, match="cannot find"):
        match(x, levels, fail_missing=True)

    with pytest.raises(ValueError, match="cannot find"):
        match(x, levels, dtype=numpy.uint32)

    mm = match(["A", "C", "B", "D", "C"], levels, fail_missing=True)
    assert list(mm) == [3, 1, 2, 0, 1]


def test_match_Factor():
    x = Factor.from_sequence(["A", "C", "B", "D", "A", "A", "C", "D", "B"])
    levels = Factor.from_sequence(["D", "C", "B", "A"])

    mm = match(x, levels)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    assert mm.dtype == numpy.dtype("int8")

    mm = match(x, levels, fail_missing=True, dtype=numpy.uint32)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    assert mm.dtype == numpy.dtype("uint32")

    # Also works when only one of these is a factor.
    mm = match(list(x), levels)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    mm = match(x, list(levels))
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]


def test_match_Factor_duplicates():
    x = Factor.from_sequence([5, 1, 2, 3, 5, 6, 7, 7, 2, 1])
    levels = Factor.from_sequence([1, 2, 3, 3, 5, 6, 1, 7, 6])

    mm = match(x, levels)
    assert list(mm) == [4, 0, 1, 2, 4, 5, 7, 7, 1, 0]

    mm = match(x, levels, duplicate_method="last")
    assert list(mm) == [4, 6, 1, 3, 4, 8, 7, 7, 1, 6]


def test_match_Factor_none():
    x = Factor.from_sequence(["A", None, "B", "D", None, "A", "C", None, "B"])
    mm = match(x, Factor.from_sequence(["D", "C", "B", "A"]))
    assert list(mm) == [3, -1, 2, 0, -1, 3, 1, -1, 2]

    lev = Factor.from_sequence(["D", None, "C", "B", "A"])
    mm = match(x, lev)
    assert list(mm) == [4, 1, 3, 0, 1, 4, 2, 1, 3]

    mm = match(x, lev, incomparables=set([None]))
    assert list(mm) == [4, -1, 3, 0, -1, 4, 2, -1, 3]

    with pytest.raises(match="cannot find"):
        match(x, lev, incomparables=set([None]), fail_missing=True)


def test_match_Factor_fail_missing():
    x = Factor.from_sequence(["A", "E", "B", "D", "E"])
    levels = Factor.from_sequence(["D", "C", "B", "A"])

    mm = match(x, levels)
    assert list(mm) == [3, -1, 2, 0, -1]

    with pytest.raises(ValueError, match="cannot find"):
        match(x, levels, fail_missing=True)

    with pytest.raises(ValueError, match="cannot find"):
        match(x, levels, dtype=numpy.uint32)

    mm = match(Factor.from_sequence(["A", "C", "B", "D", "C"]), levels, fail_missing=True)
    assert list(mm) == [3, 1, 2, 0, 1]
