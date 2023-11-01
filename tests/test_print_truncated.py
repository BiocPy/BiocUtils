from biocutils import print_truncated_list, print_truncated_dict, print_truncated


def test_print_truncated_list():
    assert print_truncated_list(range(6)) == repr(list(range(6)))
    assert print_truncated_list(range(10)) == repr(list(range(10)))
    assert print_truncated_list(range(200)) == "[0, 1, 2, ..., 197, 198, 199]"
    assert (
        print_truncated_list(
            ["A", "B", "C", "D", "E", "F"], transform=lambda x: repr("foo_" + x)
        )
        == "['foo_A', 'foo_B', 'foo_C', 'foo_D', 'foo_E', 'foo_F']"
    )
    assert (
        print_truncated_list(
            ["A", "B", "C", "D", "E", "F"],
            truncated_to=2,
            full_threshold=5,
            transform=lambda x: repr("foo_" + x),
        )
        == "['foo_A', 'foo_B', ..., 'foo_E', 'foo_F']"
    )
    assert (
        print_truncated_list(range(200), sep=" ", include_brackets=False)
        == "0 1 2 ... 197 198 199"
    )


def test_print_truncated_dict():
    assert print_truncated_dict({"A": "B"}) == "{'A': 'B'}"
    assert (
        print_truncated_dict({"A": "B", "C": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})
        == "{'A': 'B', 'C': [1, 2, 3, ..., 9, 10, 11]}"
    )
    assert (
        print_truncated_dict(
            {"A": -1, "B": 0, "C": 1, "D": 2, "E": True, "F": False},
            truncated_to=2,
            full_threshold=5,
        )
        == "{'A': -1, 'B': 0, ..., 'E': True, 'F': False}"
    )
    assert (
        print_truncated_dict(
            {"A": -1, "B": 0, "C": 1, "D": 2, "E": True, "F": False},
            sep=" ",
            include_brackets=False,
        )
        == "'A': -1 'B': 0 'C': 1 'D': 2 'E': True 'F': False"
    )


def test_print_truncated():
    internal = {"A": -1, "B": 0, "C": 1, "D": 2, "E": True, "F": False}
    expected = "{'A': -1, 'B': 0, ..., 'E': True, 'F': False}"
    assert (
        print_truncated([internal] * 10, truncated_to=2, full_threshold=5)
        == "[" + (expected + ", ") * 2 + "..." + (", " + expected) * 2 + "]"
    )
