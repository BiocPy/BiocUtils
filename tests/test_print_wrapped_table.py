from biocutils import print_wrapped_table, create_floating_names, truncate_strings, print_type
import numpy as np


def test_print_wrapped_table():
    contents = [
        ["asdasd", "1", "2", "3", "4"],
        [""] + ["|"] * 4,
        ["asyudgausydga", "A", "B", "C", "D"],
    ]
    print(print_wrapped_table(contents))
    print(print_wrapped_table(contents, floating_names=["", "aarg", "boo", "ffoo", "stuff"]))
    print(print_wrapped_table(contents, window=10))
    print(
        print_wrapped_table(
            contents, window=10, floating_names=["", "AAAR", "BBBB", "XXX", "STUFF"]
        )
    )


def test_create_floating_names():
    assert create_floating_names(None, [1,2,3,4]) == [ "[1]", "[2]", "[3]", "[4]" ]
    assert create_floating_names(["A", "B", "C", "D", "E", "F"], [1,2,3,4]) == [ "B", "C", "D", "E" ]


def test_truncate_strings():
    ref = ["A"*10, "B"*20, "C"*30]
    assert truncate_strings(ref, width=25) == [ "A"*10, "B"*20, "C"*22 + "..." ]


def test_print_type():
    assert print_type(np.array([1,2,3])) == "ndarray[int64]"
    assert print_type(np.array([1,2.5,3.3])) == "ndarray[float64]"
    assert print_type([1,2,3]) == "list"
