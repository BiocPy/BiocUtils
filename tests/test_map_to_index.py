from biocutils import map_to_index


def test_map_to_index_simple():
    mapping = map_to_index(["A", "B", "C", "D"])
    assert mapping == { "A": 0, "B": 1, "C": 2, "D": 3 }

def test_map_to_index_duplicates():
    duplicated = ["A", "B", "C", "D", "A", "B", "C", "D"]

    mapping = map_to_index(duplicated)
    assert mapping == { "A": 0, "B": 1, "C": 2, "D": 3 }

    mapping = map_to_index(["A", "B", "C", "D", "A", "B", "C", "D"], duplicate_method="last")
    assert mapping == { "A": 4, "B": 5, "C": 6, "D": 7 }

def test_map_to_index_none():
    noney = [ None, "A", None, "B", None, "C", None, "D", None ]
    mapping = map_to_index(noney)
    assert mapping == { "A": 1, "B": 3, "C": 5, "D": 7 }
