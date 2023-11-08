from biocutils import show_as_cell


def test_show_as_cell():
    assert show_as_cell([1, 2, 3, 4], range(4)) == ["1", "2", "3", "4"]
    assert show_as_cell([1, 2, 3, 4], [1, 3]) == ["2", "4"]
