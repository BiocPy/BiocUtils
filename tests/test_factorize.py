from biocutils import factorize, Factor


def test_factorize_simple():
    lev, ind = factorize([1, 3, 5, 5, 3, 1])
    assert lev == [1, 3, 5]
    assert list(ind) == [0, 1, 2, 2, 1, 0]

    # Preserves the order.
    lev, ind = factorize(["C", "D", "A", "B", "C", "A"])
    assert lev == ["C", "D", "A", "B"]
    assert list(ind) == [0, 1, 2, 3, 0, 2]

    # Handles None-ness.
    lev, ind = factorize([1, None, 5, None, 3, None])
    assert lev == [1, 5, 3]
    assert list(ind) == [0, -1, 1, -1, 2, -1]


def test_factorize_levels():
    revlev = [5, 4, 3, 2, 1]
    lev, ind = factorize([1, 3, 5, 5, 3, 1], levels=revlev)
    assert lev == revlev
    assert list(ind) == [4, 2, 0, 0, 2, 4]

    # Preserves duplicates.
    duplicated = [5, 4, 5, 4, 3, 4, 2, 3, 1, 1, 2]
    lev, ind = factorize([1, 3, 5, 5, 3, 1], levels=duplicated)
    assert lev == duplicated
    assert list(ind) == [8, 4, 0, 0, 4, 8]

    # Ignores None.
    noney = [None, 1, 2, 3, 4, 5, None]
    lev, ind = factorize([1, 3, 5, 5, 3, 1], levels=noney)
    assert lev == noney
    assert list(ind) == [1, 3, 5, 5, 3, 1]


def test_factorize_sorted():
    lev, ind = factorize(["C", "D", "A", "B", "C", "A"], sort_levels=True)
    assert lev == ["A", "B", "C", "D"]
    assert list(ind) == [2, 3, 0, 1, 2, 0]

    # Not affected if you supply the levels directly.
    lev, ind = factorize(
        ["C", "D", "A", "B", "C", "A"], levels=["D", "C", "B", "A"], sort_levels=True
    )
    assert lev == ["D", "C", "B", "A"]
    assert list(ind) == [1, 0, 3, 2, 1, 3]


def test_factorize_factor():
    f = Factor([4, 3, 2, 1, 0], ["A", "B", "C", "D", "E"])
    lev, ind = factorize(f)
    assert lev == ["E", "D", "C", "B", "A"]
    assert list(ind) == [0, 1, 2, 3, 4]

    lev, ind = factorize(f, sort_levels=True)
    assert lev == f.levels.as_list()
    assert list(ind) == [4, 3, 2, 1, 0]
