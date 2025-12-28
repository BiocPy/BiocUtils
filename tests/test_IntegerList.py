import biocutils
from biocutils import IntegerList, NamedList


def test_IntegerList_init():
    x = IntegerList([1,2,3,4])
    assert isinstance(x, IntegerList)
    assert x.as_list() == [ 1, 2, 3, 4 ]
    assert x.get_names() is None

    # Constructor works with other IntegerList objects.
    recon = IntegerList(x)
    assert recon.as_list() == x.as_list()

    empty = IntegerList()
    assert empty.as_list() == []

    # Constructor works with Nones.
    x = IntegerList([1,None,None,4])
    assert x.as_list() == [ 1, None, None, 4 ]

    # Constructor works with other NamedList objects.
    x = NamedList([True, False, None, 2.5])
    recon = IntegerList(x)
    assert recon.as_list() == [1, 0, None, 2]


def test_IntegerList_getitem():
    x = IntegerList([1,2,3,4])

    assert x[0] == 1
    sub = x[1:3]
    assert isinstance(sub, IntegerList)
    assert sub.as_list() == [2, 3]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    assert x["C"] == 3
    sub = x[["C", "D", "A", "B"]]
    assert isinstance(sub, IntegerList)
    assert sub.as_list() == [3, 4, 1, 2]


def test_IntegerList_setitem():
    x = IntegerList([1,2,3,4])
    x[0] = None
    assert x.as_list() == [None, 2, 3, 4]
    x[0] = 12345
    assert x.as_list() == [12345, 2, 3, 4]

    x[1:3] = [10, 20]
    assert x.as_list() == [12345, 10, 20, 4]

    x[0:4:2] = [None, None]
    assert x.as_list() == [None, 10, None, 4]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x["C"] = 3
    assert x.as_list() == [None, 10, 3, 4]
    x[["A", "B"]] = [True, False]
    assert x.as_list() == [1, 0, 3, 4]
    x["E"] = "50"
    assert x.as_list() == [1, 0, 3, 4, 50]
    assert x.get_names().as_list() == [ "A", "B", "C", "D", "E" ]


def test_IntegerList_mutations():
    # Insertion:
    x = IntegerList([1,2,3,4])
    x.insert(2, None)
    x.insert(1, "FOO")
    assert x.as_list() == [ 1, None, 2, None, 3, 4 ]

    # Extension:
    x.extend([None, 1, True])
    assert x.as_list() == [ 1, None, 2, None, 3, 4, None, 1, 1 ]
    alt = IntegerList([ 5, 6, 7 ])
    x.extend(alt)
    assert x.as_list() == [ 1, None, 2, None, 3, 4, None, 1, 1, 5, 6, 7 ]

    # Appending:
    x.append(1)
    assert x[-1] == 1
    x.append(None)
    assert x[-1] == None


def test_IntegerList_generics():
    x = IntegerList([1,2,3,4])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, IntegerList)
    assert sub.as_list() == [1, 4, 3, 2]

    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, IntegerList)
    assert com.as_list() == [1, 2, 3, 4, None, None, None, None]

    ass = biocutils.assign_sequence(x, [1,3], ["a", "b"])
    assert isinstance(ass, IntegerList)
    assert ass.as_list() == [1, None, 3, None]
