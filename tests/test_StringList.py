import biocutils
from biocutils import StringList


def test_StringList_basics():
    x = StringList([1,2,3,4])
    assert isinstance(x, StringList)
    assert x == [ '1', '2', '3', '4' ]
    assert x[0] == "1"

    # Constructor works with other StringList objects.
    assert StringList(x) == x

    empty = StringList()
    assert empty == []
    assert isinstance(empty, StringList)

    # Slicing works correctly.
    sub = x[1:3]
    assert isinstance(sub, StringList)
    assert sub == ["2", "3"]

    # Constructor works with Nones.
    x = StringList([1,None,None,4])
    assert x == [ '1', None, None, '4' ]

    # Copying works.
    z = x.copy()
    z[0] = "Aaron"
    assert z == [ "Aaron", None, None, "4" ]
    assert x == [ "1", None, None, "4" ]


def test_StringList_setitem():
    x = StringList([1,2,3,4])
    x[0] = None
    assert x == [None, "2", "3", "4"]
    x[0] = 12345 
    assert x == ["12345", "2", "3", "4"]

    x[1:3] = [10, 20]
    assert x == ["12345", "10", "20", "4"]

    x[0:4:2] = [None, None]
    assert x == [None, "10", None, "4"]

    alt = StringList([ "YAY", "FOO", "BAR", "WHEE" ])
    x[:] = alt
    assert x == alt


def test_StringList_mutations():
    # Insertion:
    x = StringList([1,2,3,4])
    x.insert(2, None)
    x.insert(1, "FOO")
    assert x == [ "1", "FOO", "2", None, "3", "4" ]

    # Extension:
    x.extend([None, 1, True])
    assert x == [ "1", "FOO", "2", None, "3", "4", None, "1", "True" ]
    alt = StringList([ "YAY", "BAR", "WHEE" ])
    x.extend(alt)
    assert x == [ "1", "FOO", "2", None, "3", "4", None, "1", "True", "YAY", "BAR", "WHEE" ]

    # Appending:
    x.append(1)
    assert x[-1] == "1"
    x.append(None)
    assert x[-1] == None


def test_StringList_addition():
    x1 = StringList([1,2,3,4])
    assert x1 + [5,6,7] == ["1", "2", "3", "4", "5", "6", "7"]

    x2 = StringList([5,6,7])
    assert x1 + x2 == ["1", "2", "3", "4", "5", "6", "7"]

    x1 += x2
    assert x1 == ["1", "2", "3", "4", "5", "6", "7"]


def test_StringList_generics():
    x = StringList([1,2,3,4])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, StringList)
    assert sub == ["1", "4", "3", "2"]
    
    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, StringList)
    assert com == ["1", "2", "3", "4", "a", "b", "c", "d"]
