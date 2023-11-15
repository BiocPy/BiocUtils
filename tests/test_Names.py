import biocutils
import pytest
from biocutils import Names
from copy import deepcopy


def test_Names_basics():
    x = Names([1,2,3,4])
    assert isinstance(x, Names)
    assert x.as_list() == [ "1","2","3","4" ]

    assert x.map("1") == 0
    assert x.map("4") == 3
    assert x.map("Aaron") == -1

    # Constructor works with other Names objects.
    y = Names(x)
    assert y == x

    empty = Names()
    assert empty.as_list() == []
    assert isinstance(empty, Names)

    # Slicing works correctly.
    sub = x[1:3]
    assert isinstance(sub, Names)
    assert sub.as_list() == ["2", "3"]

    # Copying works.
    z = deepcopy(x)
    z[0] = "Aaron"
    assert z.as_list() == [ "Aaron", "2", "3", "4" ]
    assert x.as_list() == [ "1", "2", "3", "4" ]


def test_Names_setitem():
    x = Names([1,2,3,4])
    x[0] = None
    assert x.as_list() == ["None", "2", "3", "4"]
    assert x.map("None") == 0
    assert x.map("1") == -1

    x[0] = 12345 
    assert x.as_list() == ["12345", "2", "3", "4"]
    assert x.map("None") == -1
    assert x.map("12345") == 0

    x[1:3] = [10, 20]
    assert x.as_list() == ["12345", "10", "20", "4"]

    alt = Names([ "YAY", "FOO", "BAR", "WHEE" ])
    x[:] = alt
    assert x == alt


def test_Names_mutations():
    # Insertion:
    x = Names([1,2,3,4])
    assert x.map("3") == 2 
    x.insert(2, None)
    assert x.map("1") == 0
    assert x.map("3") == 3
    x.insert(1, "FOO")
    assert x.map("3") == 4
    assert x.as_list() == [ "1", "FOO", "2", "None", "3", "4" ]

    # Extension:
    x = Names([1,2,3,4])
    x.extend([None, 1, True])
    assert x.as_list() == [ "1", "2", "3", "4", "None", "1", "True" ]
    assert x.map("None") == 4
    assert x.map("1") == 0
    x.extend([False, 2, None])
    assert x.as_list() == [ "1", "2", "3", "4", "None", "1", "True", "False", "2", "None" ]
    assert x.map("None") == 4
    assert x.map("False") == 7
    assert x.map("2") == 1

    # Appending:
    x = Names([1,2,3,4])
    x.append(1)
    assert x[-1] == "1"
    assert x.map("1") == 0
    x.append(None)
    assert x[-1] == "None"
    assert x.map("None") == 5


def test_Names_addition():
    x1 = Names([1,2,3,4])
    summed = x1 + [5,6,7]
    assert summed.as_list() == ["1", "2", "3", "4", "5", "6", "7"]

    x2 = Names([5,6,7])
    summed = x1 + x2
    assert summed.as_list() == ["1", "2", "3", "4", "5", "6", "7"]

    x1 += x2
    assert x1.as_list() == ["1", "2", "3", "4", "5", "6", "7"]


def test_Names_generics():
    x = Names([1,2,3,4])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, Names)
    assert sub.as_list() == ["1", "4", "3", "2"]
    
    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, Names)
    assert com.as_list() == ["1", "2", "3", "4", "a", "b", "c", "d"]

    y = ["b", "c"]
    ass = biocutils.assign_sequence(x, range(1, 3), y)
    assert isinstance(ass, Names)
    assert ass.as_list() == ["1", "b", "c", "4"]

