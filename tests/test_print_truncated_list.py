from biocutils import print_truncated_list


def test_print_truncated_list():
    assert print_truncated_list(range(6)) == repr(list(range(6)))
    assert print_truncated_list(range(10)) == repr(list(range(10)))
    assert print_truncated_list(range(200)) == "[0, 1, 2, ..., 197, 198, 199]"
    assert print_truncated_list(["A", "B", "C", "D", "E", "F"], transform=lambda x : "foo_" + x) == "['foo_A', 'foo_B', 'foo_C', 'foo_D', 'foo_E', 'foo_F']"
    assert print_truncated_list(["A", "B", "C", "D", "E", "F"], truncated_to=2, full_threshold=5, transform=lambda x : "foo_" + x) == "['foo_A', 'foo_B', ..., 'foo_E', 'foo_F']"
    assert print_truncated_list(range(200), sep=" ", include_brackets=False) == "0 1 2 ... 197 198 199"
