import biocutils
import pytest
from biocutils import NamedList
from copy import deepcopy


def test_NamedList_init():
    x = NamedList([1,2,3,4], names=['a', 'b', 'c', 'd'])
    assert isinstance(x, NamedList)
    assert x.get_data() == [ 1,2,3,4 ]
    assert x.get_names() == ["a", "b", "c", "d"]
    assert len(x) == 4

    y = NamedList(x)
    assert y.get_data() == [1,2,3,4]
    assert y.get_names() is None # names are not carried over; this is intended, and not a bug.

    empty = NamedList()
    assert empty.get_data() == []
    assert empty.get_names() is None
    assert len(empty) == 0

    x = NamedList([1,2,3,4])
    assert x.get_data() == [1,2,3,4]
    assert x.get_names() is None


def test_NamedList_get_value():
    x = NamedList([1,2,3,4])
    assert x.get_value(0) == 1
    assert x.get_value(-1) == 4
    with pytest.raises(KeyError) as ex:
        x.get_value("Aaron")
    assert str(ex.value).find("Aaron") >= 0

    x.set_names(["a", "b", "c", "d"], in_place=True)
    assert x.get_value("a") == 1
    assert x.get_value("b") == 2
    with pytest.raises(KeyError) as ex:
        x.get_value("Aaron")
    assert str(ex.value).find("Aaron") >= 0


def test_NamedList_get_slice():
    x = NamedList([1,2,3,4])

    sub = x.get_slice([0, 2])
    assert sub.get_data() == [1, 3]
    assert sub.get_names() is None

    sub = x.get_slice([False, True, True, False])
    assert sub.get_data() == [2, 3]
    assert sub.get_names() is None

    with pytest.raises(Exception) as ex:
        x.get_slice(["Aaron", "Foo"])
    assert str(ex.value).find("no names") >= 0

    x.set_names(["a", "b", "c", "d"], in_place=True)
    sub = x.get_slice([0, 2])
    assert sub.get_data() == [1, 3]
    assert sub.get_names() == ["a", "c"]

    sub = x.get_slice(["a", "d"])
    assert sub.get_data() == [1, 4]
    assert sub.get_names() == ["a", "d"]

#    with pytest.raises(Exception) as ex:
#        x.get_slice(["Aaron"])
#    assert str(ex.value).find("Aaron") >= 0


def test_NamedList_get_item():
    x = NamedList([1,2,3,4], names=["a", "b", "c", "d"])
    assert x[0] == 1
    assert x["b"] == 2
    assert x[[0, 1]].get_data() == [1,2]
    assert x[["b","d"]].get_data() == [2,4]


def test_NamedList_dict():
    x = NamedList([1,2,3,4], names=['a', 'b', 'c', 'd'])
    assert x.as_dict() == { "a": 1, "b": 2, "c": 3, "d": 4 }

    x = NamedList.from_dict({ "c": 4, "d": 5, 23: 99 })
    assert x.get_names() == [ "c", "d", "23" ]
    assert x.get_data() == [ 4, 5, 99 ]


def test_NamedList_set_value():
    x = NamedList([1,2,3,4])
    y = x.set_value(0, 10)
    assert y.get_data() == [10, 2, 3, 4]
    y = x.set_value(-1, 40)
    assert y.get_data() == [1, 2, 3, 40]

    y = x.set_value("Aaron", 10)
    assert y.get_data() == [1, 2, 3, 4, 10]
    assert y.get_names() == ["", "", "", "", "Aaron"]

    x.set_names(["a", "b", "c", "d"], in_place=True)
    y = x.set_value("a", 10)
    assert y.get_data() == [10, 2, 3, 4]
    y = x.set_value("d", 40)
    assert y.get_data() == [1, 2, 3, 40]
    y = x.set_value("Aaron", 10)
    assert y.get_data() == [1, 2, 3, 4, 10]
    assert y.get_names() == ["a", "b", "c", "d", "Aaron"]


def test_NamedList_set_slice():
    x = NamedList([1,2,3,4])
    y = x.set_slice([0, 3], [10, 40])
    assert y.get_data() == [10, 2, 3, 40]
    y = x.set_slice([False, True, True, False], [20, 30])
    assert y.get_data() == [1, 20, 30, 4]
    with pytest.raises(IndexError) as ex:
        x.set_slice(["Aaron"], [10])
    assert str(ex.value).find("no names") >= 0

    x.set_names(["a", "b", "c", "d"], in_place=True)
    y = x.set_slice(["a", "d"], [10, 40])
    assert y.get_data() == [10, 2, 3, 40]
#    with pytest.raises(KeyError) as ex:
#        y = x.set_slice(["Aaron"], [10])
#    assert str(ex.value).find("Aaron") >= 0


def test_NamedList_setitem():
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    x[0] = None
    assert x.get_data() == [None, 2, 3, 4]
    x["B"] = None
    assert x.get_data() == [None, None, 3, 4]
    x[["C", "D"]] = [30, 40]
    assert x.get_data() == [None, None, 30, 40]
    x["E"] = "FOO"
    assert x.get_data() == [None, None, 30, 40, "FOO"]
    assert x.get_names() == ["A", "B", "C", "D", "E"]


def test_NamedList_insert():
    x = NamedList([1,2,3,4])
    y = x.safe_insert(2, "FOO")
    assert y.get_data() == [1, 2, "FOO", 3, 4]
    assert y.get_names() is None

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x.insert(2, "FOO")
    assert x.get_data() == [1, 2, "FOO", 3, 4]
    assert x.get_names() == ["A", "B", "", "C", "D"]

    x.insert("D", None)
    assert x.get_data() == [1, 2, "FOO", 3, None, 4]
    assert x.get_names() == [ "A", "B", "", "C", "", "D"]


def test_NamedList_extend():
    x = NamedList([1,2,3,4])
    y = x.safe_extend([None, 1, True])
    assert y.get_data() == [ 1, 2, 3, 4, None, 1, True ]
    assert y.get_names() is None

    y = x.safe_extend(NamedList([False, 2, None], names=[ "E", "F", "G" ]))
    assert y.get_data() == [ 1, 2, 3, 4, False, 2, None ]
    assert y.get_names() == [ "", "", "", "", "E", "F", "G" ]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x.extend([None, 1, True])
    assert x.get_data() == [ 1, 2, 3, 4, None, 1, True ]
    assert x.get_names() == [ "A", "B", "C", "D", "", "", "" ]

    x.extend(NamedList([False, 2, None], names=[ "E", "F", "G" ]))
    assert x.get_data() == [ 1, 2, 3, 4, None, 1, True, False, 2, None ]
    assert x.get_names() == [ "A", "B", "C", "D", "", "", "", "E", "F", "G" ]


def test_NamedList_append():
    x = NamedList([1,2,3,4])
    y = x.safe_append(1)
    assert y.get_data() == [ 1,2,3,4,1 ]
    assert y.get_names() is None

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x.append(1)
    assert x.get_data() == [ 1,2,3,4,1 ]
    assert x.get_names() == [ "A", "B", "C", "D", "" ]


def test_NamedList_addition():
    x1 = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    summed = x1 + [5,6,7]
    assert summed.get_data() == [1, 2, 3, 4, 5, 6, 7]
    assert summed.get_names() == [ "A", "B", "C", "D", "", "", "" ]

    x2 = NamedList([5,6,7], names=["E", "F", "G"])
    summed = x1 + x2
    assert summed.get_data() == [1, 2, 3, 4, 5, 6, 7]
    assert summed.get_names() == ["A", "B", "C", "D", "E", "F", "G"]

    x1 += x2
    assert x1.get_data() == [1, 2, 3, 4, 5, 6, 7]
    assert x1.get_names() == ["A", "B", "C", "D", "E", "F", "G"]


def test_NamedList_copy():
    x = NamedList([1,2,3,4])
    y = x.copy()
    assert y.get_data() == x.get_data()
    assert y.get_names() is None

    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    y = deepcopy(x)
    assert y.get_data() == x.get_data()
    assert y.get_names() == x.get_names()


def test_NamedList_generics():
    x = NamedList([1,2,3,4], names=["A", "B", "C", "D"])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, NamedList)
    assert sub.get_data() == [1, 4, 3, 2]
    assert sub.get_names() == [ "A", "D", "C", "B" ]
    
    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, NamedList)
    assert com.get_data() == [1, 2, 3, 4, "a", "b", "c", "d"]
    assert com.get_names() == [ "A", "B", "C", "D", "", "", "", "" ]

    y = biocutils.assign_sequence(x, [1, 3], [ 20, 40 ])
    assert y.get_data() == [ 1, 20, 3, 40 ]
    assert y.get_names() == [ "A", "B", "C", "D" ]

    y = biocutils.assign_sequence(x, [1, 3], NamedList([ 20, 40 ], names=["b", "d" ]))
    assert y.get_data() == [ 1, 20, 3, 40 ]
    assert y.get_names() == [ "A", "B", "C", "D" ] # doesn't set the names, as per policy.
