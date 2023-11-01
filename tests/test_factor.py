from biocutils import factor


def test_factor_simple():
    lev, ind = factor([1, 3, 5, 5, 3, 1])
    assert lev == [1, 3, 5]
    assert ind == [0, 1, 2, 2, 1, 0]

    # Preserves the order.
    lev, ind = factor(["C", "D", "A", "B", "C", "A"])
    assert lev == ["C", "D", "A", "B"]
    assert ind == [0, 1, 2, 3, 0, 2]

    # Handles None-ness.
    lev, ind = factor([1, None, 5, None, 3, None])
    assert lev == [1, 5, 3]
    assert ind == [0, None, 1, None, 2, None]


def test_factor_levels():
    revlev = [5, 4, 3, 2, 1]
    lev, ind = factor([1, 3, 5, 5, 3, 1], levels=revlev)
    assert lev == revlev
    assert ind == [4, 2, 0, 0, 2, 4]

    # Preserves duplicates.
    duplicated = [5, 4, 5, 4, 3, 4, 2, 3, 1, 1, 2]
    lev, ind = factor([1, 3, 5, 5, 3, 1], levels=duplicated)
    assert lev == duplicated
    assert ind == [8, 4, 0, 0, 4, 8]

    # Ignores None.
    noney = [None, 1, 2, 3, 4, 5, None]
    lev, ind = factor([1, 3, 5, 5, 3, 1], levels=noney)
    assert lev == noney
    assert ind == [1, 3, 5, 5, 3, 1]


def test_factor_sorted():
    lev, ind = factor(["C", "D", "A", "B", "C", "A"], sort_levels=True)
    assert lev == ["A", "B", "C", "D"]
    assert ind == [2, 3, 0, 1, 2, 0]

    # Not affected if you supply the levels directly.
    lev, ind = factor(
        ["C", "D", "A", "B", "C", "A"], levels=["D", "C", "B", "A"], sort_levels=True
    )
    assert lev == ["D", "C", "B", "A"]
    assert ind == [1, 0, 3, 2, 1, 3]
