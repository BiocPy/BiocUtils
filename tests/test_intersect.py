from biocutils import intersect


def test_intersect_simple():
    assert intersect() == []

    y = ["B", "C", "A", "D", "E"]
    out = intersect(y)
    assert out == y

    out = intersect(y, ["A", "C", "E"])
    assert out == ["C", "A", "E"]

    out = intersect(y, ["A", "C", "E"], ["E", "A"])
    assert out == ["A", "E"]


def test_intersect_duplicates():
    # Doesn't report B, D, or F, despite the fact they have multiple counts.
    out = intersect(["B", "B", "C", "A", "D", "D", "E"], ["A", "A", "C", "E", "F", "F"])
    assert out == ["C", "A", "E"]

    # Doesn't report A multiple times.
    out = intersect(["C", "A", "D", "A", "E", "A"], ["A", "C", "E", "F"])
    assert out == ["C", "A", "E"]

    # Switches the order of A being reported.
    out = intersect(
        ["C", "A", "D", "A", "E", "A"], ["A", "C", "E", "F"], duplicate_method="last"
    )
    assert out == ["C", "E", "A"]

    # Handles the single case correctly.
    single = ["A", "B", "A", "C", "D", "E", "D", "C"]
    out = intersect(single)
    assert out == ["A", "B", "C", "D", "E"]

    out = intersect(single, duplicate_method="last")
    assert out == ["B", "A", "E", "D", "C"]


def test_intersect_none():
    y = ["B", None, "C", "A", None, "D", "E"]
    out = intersect(y)
    assert out == ["B", "C", "A", "D", "E"]

    out = intersect(y, ["A", None, "C", "E", None, "F"])
    assert out == ["C", "A", "E"]
