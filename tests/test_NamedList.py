import biocutils
import pytest
from biocutils import NamedList


def test_NamedList_basics():
    x = NamedList([1,2,3,4], names=['a', 'b', 'c', 'd'])
    assert isinstance(x, NamedList)
    assert x == [ 1,2,3,4 ]
    assert x.get_names() == ["a", "b", "c", "d"]

    assert x["a"] == 1
    assert x["b"] == 2
    with pytest.raises(KeyError) as ex:
        x["Aaron"]
    assert str(ex.value).find("Aaron") >= 0

    # Constructor works with other NamedList objects.
    y = NamedList(x)
    assert y == x
    assert y.get_names() == ["a", "b", "c", "d"]

    empty = NamedList()
    assert empty == []
    assert isinstance(empty, NamedList)
    assert empty.get_names() == []

    # Slicing works correctly.
    sub = x[1:3]
    assert isinstance(sub, NamedList)
    assert sub == [2, 3]
    assert sub.get_names() == ["b", "c"]

    # Copying works.
    z = x.copy()
    z[0] = "Aaron"
    assert z == [ "Aaron", 2, 3, 4 ]
    assert x == [ 1, 2, 3, 4 ]
    assert z.get_names() == [ "a", "b", "c", "d" ]


def test_NamedList_dict():
    x = NamedList([1,2,3,4], names=['a', 'b', 'c', 'd'])
    assert x.as_dict() == { "a": 1, "b": 2, "c": 3, "d": 4 }

    x = NamedList({ "c": 4, "d": 5, 23: 99 })
    assert x.get_names() == [ "c", "d", "23" ]
    assert x == [ 4, 5, 99 ]


def test_NamedList_setitem():
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    x[0] = None
    assert x == [None, 2, 3, 4]
    assert x["A"] == None

    # Replacing by name.
    x["B"] = "FOO"
    assert x[1] == "FOO"

    # Replacing slices.
    x[1:3] = [10, 20]
    assert x == [None, 10, 20, 4]
    x[1:3] = NamedList([4,5], names=["YAY", "BAR"])
    assert x == [None, 4, 5, 4]
    assert x.get_names() == [ "A", "YAY", "BAR", "D" ]

    # Appending by name.
    x["Aaron"] = "BAR"
    assert x["Aaron"] == "BAR"


def test_NamedList_mutations():
    # Insertion:
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    x.insert(2, "FOO")
    assert x == [1, 2, "FOO", 3, 4]
    assert x.get_names() == [ "A", "B", "", "C", "D"]
    x.insert("D", None)
    assert x == [1, 2, "FOO", 3, None, 4]
    assert x.get_names() == [ "A", "B", "", "C", "", "D"]

    # Extension:
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    x.extend([None, 1, True])
    assert x == [ 1, 2, 3, 4, None, 1, True ]
    assert x.get_names() == [ "A", "B", "C", "D", "", "", "" ]
    x.extend(NamedList([False, 2, None], names=[ "E", "F", "G" ]))
    assert x == [ 1, 2, 3, 4, None, 1, True, False, 2, None ]
    assert x.get_names() == [ "A", "B", "C", "D", "", "", "", "E", "F", "G" ]

    # Appending:
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    x.append(1)
    assert x == [ 1,2,3,4,1 ]
    assert x.get_names() == [ "A", "B", "C", "D", "" ]


def test_NamedList_addition():
    x1 = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    summed = x1 + [5,6,7]
    assert summed == [1, 2, 3, 4, 5, 6, 7]
    assert summed.get_names() == [ "A", "B", "C", "D", "", "", "" ]

    x2 = NamedList([5,6,7], names=["E", "F", "G"])
    summed = x1 + x2
    assert summed == [1, 2, 3, 4, 5, 6, 7]
    assert summed.get_names() == ["A", "B", "C", "D", "E", "F", "G"]

    x1 += x2
    assert x1 == [1, 2, 3, 4, 5, 6, 7]
    assert x1.get_names() == ["A", "B", "C", "D", "E", "F", "G"]


def test_NamedList_generics():
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, NamedList)
    assert sub == [1, 4, 3, 2]
    assert sub.get_names() == [ "A", "D", "C", "B" ]
    
    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, NamedList)
    assert com == [1, 2, 3, 4, "a", "b", "c", "d"]
    assert com.get_names() == [ "A", "B", "C", "D", "", "", "", "" ]

    y = biocutils.assign_sequence(x, [1, 3], [ 20, 40 ])
    assert y == [ 1, 20, 3, 40 ]
    assert y.get_names() == [ "A", "B", "C", "D" ]

    y = biocutils.assign_sequence(x, [1, 3], NamedList([ 20, 40 ], names=["b", "d" ]))
    assert y == [ 1, 20, 3, 40 ]
    assert y.get_names() == [ "A", "b", "C", "d" ]
