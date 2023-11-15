import biocutils
import pytest
from biocutils import Names
from copy import deepcopy, copy


def test_Names_init():
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


def test_Names_getters():
    x = Names([1,2,3,4])
    assert x.get_value(0) == "1"
    assert x.get_value(1) == "2"
    assert x.map("1") == 0

    sub = x.get_slice(slice(2, 4))
    assert sub.as_list() == ["3", "4"]
    assert sub.map("3") == 0
    sub = x.get_slice([True, False, True, False])
    assert sub.as_list() == ["1", "3"]
    assert sub.map("3") == 1

    assert x[3] == "4"
    sub = x[0:4:2]
    assert sub.as_list() == ["1", "3"]


def test_Names_setters():
    x = Names([1,2,3,4])
    y = x.set_value(2, "foo")
    assert y.as_list() == [ "1", "2", "foo", "4" ]
    assert y.map("3") == -1
    assert y.map("foo") == 2

    y = x.set_slice([0,3], ["foo", "bar"])
    assert y.as_list() == [ "foo", "2", "3", "bar" ]
    assert y.map("4") == -1
    assert y.map("foo") == 0

    # Doing it again so that we get some coverage on what happens
    # when the reverse map is already instantiated.
    y = x.set_value(2, None)
    assert y.map("None") == 2
    y = y.set_value(1, "foo")
    assert y.map("foo") == 1
    assert y.map("None") == 2

    y = x.set_slice([2], [None])
    assert y.map("None") == 2
    y = y.set_slice([1], ["foo"])
    assert y.map("foo") == 1
    assert y.map("None") == 2

    # Coercion to string is done correctly.
    y = x.set_value(2, 12345)
    assert y.get_value(2) == "12345"
    y = x.set_slice([1,2], [True, None])
    assert y.as_list() == [ "1", "True", "None", "4" ]

    x[3] = "blah"
    assert x.map("4") == -1
    assert x.map("blah") == 3
    x[0:4:2] = ["a", "b"]
    assert x.map("a") == 0
    assert x.map("1") == -1


def test_Names_copying():
    x = Names([1,2,3,4])
    z = copy(x)
    z[0] = "Aaron"
    assert z.as_list() == [ "Aaron", "2", "3", "4" ]
    assert x.as_list() == [ "1", "2", "3", "4" ]

    z = deepcopy(x)
    z[0] = "Aaron"
    assert z.as_list() == [ "Aaron", "2", "3", "4" ]
    assert x.as_list() == [ "1", "2", "3", "4" ]


def test_Names_insertion():
    x = Names([1,2,3,4])
    y = x.safe_insert(2, None)
    assert y.as_list() == ["1", "2", "None", "3", "4"]
    assert y.map("1") == 0
    assert y.map("3") == 3

    # Doing it in place.
    x.insert(2, None)
    assert x.map("1") == 0
    assert x.map("3") == 3

    # Doing it again so that we get some coverage on what happens
    # when the reverse map has already been instantiated.
    x.insert(1, "FOO")
    assert x.map("3") == 4
    assert x.as_list() == [ "1", "FOO", "2", "None", "3", "4" ]


def test_Names_extension():
    x = Names([1,2,3,4])
    y = x.safe_extend([None, 1, True])
    assert y.as_list() == [ "1", "2", "3", "4", "None", "1", "True" ]
    assert y.map("None") == 4
    assert y.map("1") == 0

    # Now doing it in place.
    x.extend([None, 1, True])
    assert x.as_list() == [ "1", "2", "3", "4", "None", "1", "True" ]
    assert x.map("None") == 4
    assert x.map("1") == 0

    # Doing it again so that we get some coverage on what happens
    # when the reverse map has already been instantiated.
    x.extend([False, 2, None])
    assert x.as_list() == [ "1", "2", "3", "4", "None", "1", "True", "False", "2", "None" ]
    assert x.map("None") == 4
    assert x.map("False") == 7
    assert x.map("2") == 1


def test_Names_appending():
    x = Names([1,2,3,4])
    y = x.safe_append(None)
    assert y.as_list() == [ "1", "2", "3", "4", "None" ]
    assert y.map("None") == 4

    # Now doing it in place.
    x.append(1)
    assert x[-1] == "1"
    assert x.map("1") == 0

    # Doing it again so that we get some coverage on what happens
    # when the reverse map has already been instantiated.
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

