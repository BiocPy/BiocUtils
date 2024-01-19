import biocutils
from biocutils import BooleanList, NamedList


def test_BooleanList_init():
    x = BooleanList([ True, False, False, True ])
    assert isinstance(x, BooleanList)
    assert x.as_list() == [ True, False, False, True ]
    assert x.get_names() is None

    # Constructor works with other BooleanList objects.
    recon = BooleanList(x)
    assert recon.as_list() == x.as_list()

    empty = BooleanList()
    assert empty.as_list() == []

    # Constructor works with Nones.
    x = BooleanList([True,None,None,False])
    assert x.as_list() == [ True, None, None, False ]

    # Constructor works with other NamedList objects.
    x = NamedList(["", 2, None, 0.0])
    recon = BooleanList(x)
    assert recon.as_list() == [False, True, None, False]


def test_BooleanList_getitem():
    x = BooleanList([True, False, True, False ])

    assert x[0]
    sub = x[1:3]
    assert isinstance(sub, BooleanList)
    assert sub.as_list() == [False, True]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    assert x["C"]
    sub = x[["D", "C", "A", "B"]]
    assert isinstance(sub, BooleanList)
    assert sub.as_list() == [False, True, True, False]


def test_BooleanList_setitem():
    x = BooleanList([False, True, True, False])
    x[0] = None
    assert x.as_list() == [None, True, True, False]
    x[0] = 12345 
    assert x.as_list() == [True, True, True, False]

    x[1:3] = [False, False]
    assert x.as_list() == [True, False, False, False]

    x[0:4:2] = [None, None]
    assert x.as_list() == [None, False, None, False]

    x.set_names(["A", "B", "C", "D"], in_place=True)
    x["C"] = True 
    assert x.as_list() == [None, False, True, False]
    x[["A", "B"]] = [False, True]
    assert x.as_list() == [False, True, True, False]
    x["E"] = "50"
    assert x.as_list() == [False, True, True, False, True]
    assert x.get_names().as_list() == [ "A", "B", "C", "D", "E" ]


def test_BooleanList_mutations():
    # Insertion:
    x = BooleanList([1,2,3,4])
    x.insert(2, None)
    x.insert(1, "")
    assert x.as_list() == [ True, False, True, None, True, True ]

    # Extension:
    x.extend([None, 1, 5.0 ])
    assert x.as_list() == [ True, False, True, None, True, True, None, True, True ]
    alt = BooleanList([ 0, "", 1 ])
    x.extend(alt)
    assert x.as_list() == [ True, False, True, None, True, True, None, True, True, False, False, True ]

    # Appending:
    x.append(1)
    assert x[-1]
    x.append(None)
    assert x[-1] is None


def test_BooleanList_generics():
    x = BooleanList([False, False, True, True])
    sub = biocutils.subset_sequence(x, [0,3,2,1])
    assert isinstance(sub, BooleanList)
    assert sub.as_list() == [False, True, True, False]

    y = ["a", "b", "c", "d"]
    com = biocutils.combine_sequences(x, y)
    assert isinstance(com, BooleanList)
    assert com.as_list() == [False, False, True, True, True, True, True, True]

    ass = biocutils.assign_sequence(x, [1,3], ["a", 0])
    assert isinstance(ass, BooleanList)
    assert ass.as_list() == [False, True, True, False]
