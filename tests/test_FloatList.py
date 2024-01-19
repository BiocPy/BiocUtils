import biocutils
from biocutils import FloatList, NamedList


def test_FloatList_init():
    x = FloatList([ 1.1, 2, 3, 4 ])
    assert isinstance(x, FloatList)
    assert x.as_list() == [ 1.1, 2.0, 3.0, 4.0 ]
    assert x.get_names() is None

    # Constructor works with other FloatList objects.
    recon = FloatList(x)
    assert recon.as_list() == x.as_list()

    empty = FloatList()
    assert empty.as_list() == []

    # Constructor works with Nones.
    x = FloatList([1,None,None,4.5])
    assert x.as_list() == [ 1.0, None, None, 4.5 ]

    # Constructor works with other NamedList objects.
    x = NamedList([True, False, None, 2.5])
    recon = FloatList(x)
    assert recon.as_list() == [1.0, 0.0, None, 2.5]


def test_FloatList_getitem():
    x = FloatList([ 1.5, 2.5, 3.5, 4.5])

    assert x[0] == 1.5
    sub = x[1:3]
    assert isinstance(sub, FloatList)
    assert sub.as_list() == [2.5, 3.5]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    assert x["C"] == 3.5
    sub = x[["C", "D", "A", "B"]]
    assert isinstance(sub, FloatList)
    assert sub.as_list() == [3.5, 4.5, 1.5, 2.5]


def test_FloatList_setitem():
    x = FloatList([ 0.5, -2.1, -3.2, -4.5 ])
    x[0] = None
    assert x.as_list() == [None, -2.1, -3.2, -4.5]
    x[0] = 12345 
    assert x.as_list() == [12345.0, -2.1, -3.2, -4.5]

    x[1:3] = [10.1, 20.2]
    assert x.as_list() == [12345.0, 10.1, 20.2, -4.5]

    x[0:4:2] = [None, None]
    assert x.as_list() == [None, 10.1, None, -4.5]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x["C"] = 3.2
    assert x.as_list() == [None, 10.1, 3.2, -4.5]
    x[["A", "B"]] = [True, False]
    assert x.as_list() == [1.0, 0.0, 3.2, -4.5]
    x["E"] = "50"
    assert x.as_list() == [1.0, 0.0, 3.2, -4.5, 50.0]
    assert x.get_names().as_list() == [ "A", "B", "C", "D", "E" ]


def test_FloatList_mutations():
    # Insertion:
    x = FloatList([ 1.1, 2.2, 3.3, 4.4 ])
    x.insert(2, None)
    x.insert(1, "FOO")
    assert x.as_list() == [ 1.1, None, 2.2, None, 3.3, 4.4 ]

    # Extension:
    x.extend([None, -1.5, True])
    assert x.as_list() == [ 1.1, None, 2.2, None, 3.3, 4.4, None, -1.5, 1.0 ]
    alt = FloatList([ 5.5, 6.6, 7.7 ])
    x.extend(alt)
    assert x.as_list() == [ 1.1, None, 2.2, None, 3.3, 4.4, None, -1.5, 1.0, 5.5, 6.6, 7.7 ]

    # Appending:
    x.append(-10.1)
    assert x[-1] == -10.1
    x.append(None)
    assert x[-1] == None


def test_FloatList_generics():
    x = FloatList([ 1.1, 2.2, 3.3, 4.4 ])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, FloatList)
    assert sub.as_list() == [1.1, 4.4, 3.3, 2.2]

    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, FloatList)
    assert com.as_list() == [1.1, 2.2, 3.3, 4.4, None, None, None, None]

    ass = biocutils.assign_sequence(x, [1,3], ["a", "b"])
    assert isinstance(ass, FloatList)
    assert ass.as_list() == [1.1, None, 3.3, None]
