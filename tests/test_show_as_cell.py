from biocutils import show_as_cell
import numpy


def test_show_as_cell():
    assert show_as_cell([1, 2, 3, 4], range(4)) == ["1", "2", "3", "4"]
    assert show_as_cell([1, 2, 3, 4], [1, 3]) == ["2", "4"]

    assert show_as_cell(["abcdefghijklmnopqrstuvwxy", "abcdefghijklmnopqrstuvwxyz"], [0,1]) == ["abcdefghijklmnopqrstuvwxy", "abcdefghijklmnopqrst..."]
    assert show_as_cell(["abcdefghijkl\nmnopqrstuvwxyz", "abc\ndefghijklmnopqrstuvwxyz"], [0,1]) == ["abcdefghijkl...", "abc..."]


def test_show_as_cell_numpy():
    n1d = numpy.array([1,2,3,4,5])
    assert show_as_cell(n1d, [0, 1, 4]) == ["1", "2", "5"]

    # Empty arrays are processed correctly.
    empty = numpy.ndarray((10, 0))
    assert show_as_cell(empty, [0, 1, 4]) == ["[]", "[]", "[]"]
    empty = numpy.ndarray((10, 20, 0))
    assert show_as_cell(empty, [0, 1, 2, 3]) == ["[]", "[]", "[]", "[]"]

    # Arrays where all other extents are 1 are processed correctly.
    n1col = numpy.array([1,2,3,4,5]).reshape((5, 1))
    assert show_as_cell(n1col, [2, 3]) == ["[3]", "[4]"]
    n1col = numpy.array([1,2,3,4,5]).reshape((5, 1, 1))
    assert show_as_cell(n1col, [1, 4]) == ["[[2]]", "[[5]]"]

    # Arrays other extents are > 1 are processed correctly.
    general = numpy.array([1,2,3,4,5,6]).reshape((3, 2))
    assert show_as_cell(general, [0, 2]) == ["[1 2]", "[5 6]"]
    general = numpy.array([1,2,3,4,5,6]).reshape((3, 2, 1))
    assert show_as_cell(general, [0, 2]) == ["[[1]...", "[[5]..."]
