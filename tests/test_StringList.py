import biocutils
from biocutils import StringList, NamedList


def test_StringList_init():
    x = StringList([1,2,3,4])
    assert isinstance(x, StringList)
    assert x.get_data() == [ '1', '2', '3', '4' ]
    assert x.get_names() is None

    # Constructor works with other StringList objects.
    recon = StringList(x)
    assert recon.get_data() == x.get_data()

    empty = StringList()
    assert empty.get_data() == []

    # Constructor works with Nones.
    x = StringList([1,None,None,4])
    assert x.get_data() == [ '1', None, None, '4' ]

    # Constructor works with other NamedList objects.
    x = NamedList([True, False, None, 2])
    recon = StringList(x)
    assert recon.get_data() == ["True", "False", None, "2"]


def test_StringList_getitem():
    x = StringList([1,2,3,4])

    assert x[0] == "1"
    sub = x[1:3]
    assert isinstance(sub, StringList)
    assert sub.get_data() == ["2", "3"]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    assert x["C"] == "3"
    sub = x[["C", "D", "A", "B"]]
    assert isinstance(sub, StringList)
    assert sub.get_data() == ["3", "4", "1", "2"]


def test_StringList_setitem():
    x = StringList([1,2,3,4])
    x[0] = None
    assert x.get_data() == [None, "2", "3", "4"]
    x[0] = 12345 
    assert x.get_data() == ["12345", "2", "3", "4"]

    x[1:3] = [10, 20]
    assert x.get_data() == ["12345", "10", "20", "4"]

    x[0:4:2] = [None, None]
    assert x.get_data() == [None, "10", None, "4"]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x["C"] = "3"
    assert x.get_data() == [None, "10", "3", "4"]
    x[["A", "B"]] = [True, False]
    assert x.get_data() == ["True", "False", "3", "4"]
    x["E"] = 50
    assert x.get_data() == ["True", "False", "3", "4", "50"]
    assert x.get_names() == [ "A", "B", "C", "D", "E" ]


def test_StringList_mutations():
    # Insertion:
    x = StringList([1,2,3,4])
    x.insert(2, None)
    x.insert(1, "FOO")
    assert x.get_data() == [ "1", "FOO", "2", None, "3", "4" ]

    # Extension:
    x.extend([None, 1, True])
    assert x.get_data() == [ "1", "FOO", "2", None, "3", "4", None, "1", "True" ]
    alt = StringList([ "YAY", "BAR", "WHEE" ])
    x.extend(alt)
    assert x.get_data() == [ "1", "FOO", "2", None, "3", "4", None, "1", "True", "YAY", "BAR", "WHEE" ]

    # Appending:
    x.append(1)
    assert x[-1] == "1"
    x.append(None)
    assert x[-1] == None


def test_StringList_generics():
    x = StringList([1,2,3,4])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, StringList)
    assert sub.get_data() == ["1", "4", "3", "2"]
    
    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, StringList)
    assert com.get_data() == ["1", "2", "3", "4", "a", "b", "c", "d"]

    ass = biocutils.assign_sequence(x, [1,3], ["a", "b"])
    assert isinstance(ass, StringList)
    assert ass.get_data() == ["1", "a", "3", "b"]
