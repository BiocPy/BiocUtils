from biocutils import union


def test_union_simple():
    assert union() == []

    y = ["B", "C", "A", "D", "E"]
    assert union(y) == y

    out = union(y, [ "A", "C", "E", "F" ])
    assert out == ["B", "C", "A", "D", "E", "F"]

    out = union(["B", "C", "A", "D", "E"], ["A", "C", "K", "E"], ["G", "K"])
    assert out == ["B", "C", "A", "D", "E", "K", "G"]


def test_union_duplicates():
    y1 = ["B", "B", "C", "A", "D", "D", "E"]
    y2 = ["F", "A", "A", "C", "E", "F"]

    out = union(y1, y2)
    assert out == ["B", "C", "A", "D", "E", "F"]

    out = union(y1, y2, duplicate_method = "last")
    assert out == ["B", "D", "A", "C", "E", "F"]


def test_union_none():
    out = union(
        ["B", None, "C", "A", None, "D", "E"], 
        ["A", None, "C", "E", None, "F"]
    )
    assert out == ["B", "C", "A", "D", "E", "F"]
