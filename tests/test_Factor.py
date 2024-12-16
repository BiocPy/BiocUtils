from biocutils import Factor, combine, StringList, subset_sequence, assign_sequence
import pytest
import copy
import numpy


def test_factor_init():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert len(f) == 6
    assert list(f) == ["A", "B", "C", "A", "C", "E"]
    assert list(f.get_codes()) == [0, 1, 2, 0, 2, 4]
    assert f.get_levels().as_list() == ["A", "B", "C", "D", "E"]
    assert not f.get_ordered()

    # Works with missing values.
    f = Factor([0, 1, None, 0, numpy.ma.masked, 4], levels=["A", "B", "C", "D", "E"])
    assert len(f) == 6
    assert list(f) == ["A", "B", None, "A", None, "E"]
    assert list(f.get_codes()) == [0, 1, -1, 0, -1, 4]
    
    f = Factor([None] * 10, levels=["A", "B", "C", "D", "E"])
    assert list(f) == [None] * 10

    # Works with NumPy inputs.
    f = Factor(numpy.array([4,3,2,1,0], dtype=numpy.uint8), levels=numpy.array(["A", "B", "C", "D", "E"]))
    assert len(f) == 5 
    assert f.get_codes().dtype == numpy.int8
    assert isinstance(f.get_levels(), StringList)

    with pytest.raises(ValueError) as ex:
        Factor([0, 1, 100], ["A"])
    assert str(ex.value).find("refer to an entry") >= 0

    with pytest.raises(ValueError) as ex:
        Factor([0, 1], ["A", "B", "A"])
    assert str(ex.value).find("should be unique") >= 0

    # Works with names.
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"], names=["1", "2", "3", "4", "5", "6"])
    assert f.get_names().as_list() == ["1", "2", "3", "4", "5", "6"]


def test_factor_iter():
    f = Factor([0, 1, 2, -1, 2, 4], levels=["A", "B", "C", "D", "E"])
    output = []
    for y in f:
        output.append(y)
    assert output == ["A", "B", "C", None, "C", "E"]


def test_factor_comparisons():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert f == f
    assert f != []
    f2 = f.replace_levels(["E", "C", "D", "B", "A"])
    assert f != f2
    f2 = f.set_ordered(True)
    assert f != f2
    f2 = Factor([0, 1, 2, 3, 4], levels=["A", "B", "C", "D", "E"])
    assert f != f2
    f2 = Factor([0, 1, 2, 3, 4, 0], levels=["A", "B", "C", "D", "E"])
    assert f != f2


def test_Factor_print():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert repr(f).startswith("Factor(")
    assert str(f).startswith("Factor of length")

    f = Factor([0, 1, 4, 2, 0, 3, 1, 3, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert repr(f).startswith("Factor(")
    assert str(f).startswith("Factor of length")

    f = Factor([], levels=["A", "B", "C", "D", "E"])
    assert repr(f).startswith("Factor(")
    assert str(f).startswith("Factor of length")

    f = Factor([1], levels=["A", "B", "C", "D", "E"])
    assert repr(f).startswith("Factor(")
    assert str(f).startswith("Factor of length")

    f = Factor([i % 5 for i in range(100)], levels=["A", "B", "C", "D", "E"])
    assert repr(f).startswith("Factor(")
    assert str(f).startswith("Factor of length")


def test_Factor_get_value():
    f = Factor([0, 1, 2, -1, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert f.get_value(0) == "A"
    assert f.get_value(2) == "C"
    assert f.get_value(3) == None

    f.set_names(["1", "2", "3", "4", "5", "6"], in_place=True)
    assert f.get_value("1") == "A"
    assert f.get_value("2") == "B"


def test_Factor_get_slice():
    f = Factor([0, 1, 2, -1, 2, 4], levels=["A", "B", "C", "D", "E"])

    sub = f.get_slice([0, 1]) 
    assert list(sub) == ["A", "B"]
    assert sub.get_levels() == f.get_levels()

    sub = f.get_slice([True, False] * 3)
    assert list(sub) == ["A", "C", "C"]
    assert sub.get_levels() == f.get_levels()

    f.set_names(["1", "2", "3", "4", "5", "6"], in_place=True)
    sub = f.get_slice(["4", "3", "2", "1"])
    assert list(sub) == [None, "C", "B", "A"]
    assert sub.get_levels() == f.get_levels()
    assert sub.get_names().as_list() == [ "4", "3", "2", "1" ]


def test_Factor_getitem():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    assert f[0] == "A"
    assert f[2] == "C"
    assert f[-1] == "E"

    f2 = f[2:4]
    assert list(f2.get_codes()) == [2, 0]
    assert f2.get_levels() == f.get_levels()

    f2 = f[[1, 3, 5]]
    assert list(f2.get_codes()) == [1, 0, 4]
    assert f2.get_levels() == f.get_levels()

    f2 = f[[-1, -2, -3]]
    assert list(f2.get_codes()) == [4, 2, 0]
    assert f2.get_levels() == f.get_levels()


def test_Factor_set_value():
    f = Factor([0, 1, 2, -1, 2, 4], levels=["A", "B", "C", "D", "E"])
    y = f.set_value(3, "D")
    assert y.get_value(3) == "D"

    f.set_names(["1", "2", "3", "4", "5", "6"], in_place=True)
    y = f.set_value("4", None)
    assert f.get_value(3) == None
    assert f.get_value("4") == None


def test_Factor_set_slice():
    f = Factor([0, 1, 2, 3, 2, 1], levels=["A", "B", "C", "D", "E"])
    f2 = Factor([0, 1, 2, 3, 2, 1], levels=["A", "B", "C", "D", "E"])

    y = f.set_slice(slice(2), f2[2:4])
    assert list(y.get_codes()) == [2, 3, 2, 3, 2, 1]
    assert y.get_levels() == f.get_levels()

    f2 = Factor([0, 1, 2, 3, 2, 1], levels=["E", "D", "C", "B", "A"])
    y = f.set_slice([-3, -2, -1], f2[0:3])
    assert list(y.get_codes()) == [0, 1, 2, 4, 3, 2]
    assert y.get_levels() == f.get_levels()

    f2 = Factor([0, 1, 2, 3, 2, 1], levels=["e", "d", "c", "b", "a"])
    y = f.set_slice(range(6), f2)
    assert list(y.get_codes()) == [-1] * 6
    assert y.get_levels() == f.get_levels()

    # Now throwing in some names.
    f.set_names(["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"], in_place=True)
    y = f.set_slice(["bravo", "charlie", "delta"], f[3:6])
    assert list(y.get_codes()) == [ 0, 3, 2, 1, 2, 1 ]
    assert y.get_levels() == f.get_levels()
    assert y.get_names() == f.get_names()


def test_Factor_setitem():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f[0] = "B"
    f[2] = "A"
    f[-1] = "D"
    assert list(f.get_codes()) == [1, 1, 0, 0, 2, 3]

    f[2:5] = Factor([4, 3, 1], levels=["A", "B", "C", "D", "E"]) 
    assert list(f.get_codes()) == [1, 1, 4, 3, 1, 3]
    assert f.get_levels() == f.get_levels()


def test_Factor_drop_unused_levels():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.drop_unused_levels()
    assert f2.get_levels().as_list() == ["A", "B", "C", "E"]
    assert list(f2) == list(f)

    f = Factor([3, 4, 2, 3, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.drop_unused_levels(in_place=True)
    assert f2.get_levels().as_list() == ["C", "D", "E"]
    assert list(f2) == ["D", "E", "C", "D", "C", "E"]


def test_Factor_replace_levels():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.replace_levels(["E", "D", "C", "B", "A"])
    assert f2.get_levels().as_list() == ["E", "D", "C", "B", "A"]
    assert (f2.get_codes() == f.get_codes()).all()
    assert list(f2) != list(f)

    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.replace_levels(["G", "F", "E", "D", "C", "B", "A"], in_place=True)
    assert f2.get_levels().as_list() == ["G", "F", "E", "D", "C", "B", "A"]
    assert (f2.get_codes() == f.get_codes()).all()

    with pytest.raises(ValueError, match="at least as long") as ex:
        f.replace_levels(["F"])

    with pytest.raises(ValueError, match="non-missing") as ex:
        f.replace_levels([None, "A"] * 10)
    assert str(ex.value).find("non-missing") >= 0

    with pytest.raises(ValueError, match="should be unique") as ex:
        f.replace_levels(["A"] * 10)


def test_Factor_remap_levels():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.remap_levels(["E", "D", "C", "B", "A"])
    assert f2.get_levels().as_list() == ["E", "D", "C", "B", "A"]
    assert list(f2.get_codes()) == [4, 3, 2, 4, 2, 0]
    assert list(f2) == list(f)

    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.remap_levels(["E", "C", "A"], in_place=True)
    assert f2.get_levels().as_list() == ["E", "C", "A"]
    assert list(f2.get_codes()) == [2, -1, 1, 2, 1, 0]

    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    f2 = f.remap_levels("E")  # reorders
    assert f2.get_levels().as_list() == ["E", "A", "B", "C", "D"]
    assert list(f2.get_codes()) == [1, 2, 3, 1, 3, 0]

    with pytest.raises(ValueError, match="should already be present"):
        f.remap_levels("F")

    with pytest.raises(ValueError, match="non-missing") as ex:
        f.remap_levels([None, "A"])

    with pytest.raises(ValueError, match="should be unique") as ex:
        f.remap_levels(["A", "A"])


def test_Factor_set_levels():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])

    f2 = f.set_levels(["E", "D", "C", "B", "A"], remap=False)
    assert f2.get_levels().as_list() == ["E", "D", "C", "B", "A"]
    assert (f2.get_codes() == f.get_codes()).all()

    with pytest.warns(DeprecationWarning) as ex:
        f2 = f.set_levels(["E", "D", "C", "B", "A"], remap=True)
    assert f2.get_levels().as_list() == ["E", "D", "C", "B", "A"]
    assert list(f2) == list(f)


def test_Factor_copy():
    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    out = copy.copy(f)
    assert (f.get_codes() == out.get_codes()).all()
    assert f.get_levels() == out.get_levels()

    f = Factor([0, 1, 2, 0, 2, 4], levels=["A", "B", "C", "D", "E"])
    out = copy.deepcopy(f)
    assert (f.get_codes() == out.get_codes()).all()
    assert f.get_levels() == out.get_levels()

    f.set_names(["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"], in_place=True)
    out = copy.copy(f)
    assert f.get_names() == out.get_names()


def test_Factor_generics():
    f = Factor([0,1,2,3,4], levels=["A", "B", "C", "D", "E"])
    sub = subset_sequence(f, range(2, 4))
    assert list(sub._codes) == [2, 3]
    assert sub.get_levels() == f.get_levels()

    ass = assign_sequence(f, range(2, 4), f[1:3])
    assert list(ass._codes) == [0, 1, 1, 2, 4]
    assert ass.get_levels() == f.get_levels()


def test_Factor_combine():
    # Same levels.
    f1 = Factor([0, 2, 4, 2, 0], levels=["A", "B", "C", "D", "E"])
    f2 = Factor([1, 3, 1], levels=["A", "B", "C", "D", "E"])
    out = combine(f1, f2)
    assert out.get_levels() == f2.get_levels()
    assert list(out.get_codes()) == [0, 2, 4, 2, 0, 1, 3, 1]

    # Different levels.
    f1 = Factor([0, 2, 4, 2, 0], levels=["A", "B", "C", "D", "E"])
    f2 = Factor([1, 3, 1], levels=["D", "E", "F", "G"])
    out = combine(f1, f2)
    assert out.get_levels().as_list() == ["A", "B", "C", "D", "E", "F", "G"]
    assert list(out.get_codes()) == [0, 2, 4, 2, 0, 4, 6, 4]

    f2 = Factor([1, 3, None], levels=["D", "E", "F", "G"])
    out = combine(f1, f2)
    assert list(out.get_codes()) == [0, 2, 4, 2, 0, 4, 6, -1]

    # Ordering is preserved for the same levels, lost otherwise.
    f1 = Factor([0, 2, 4, 2, 0], levels=["A", "B", "C", "D", "E"], ordered=True)
    f2 = Factor([1, 3, 1], levels=["A", "B", "C", "D", "E"], ordered=True)
    out = combine(f1, f2)
    assert out.get_ordered()

    f2 = Factor([1, 3, 2], levels=["D", "E", "F", "G"], ordered=True)
    out = combine(f1, f2)
    assert not out.get_ordered()

    # Checking that names are correctly combined.
    print(f1)
    named = f2.set_names(["alpha", "bravo", "charlie"])
    out = combine(f1, named)
    assert out.get_names().as_list() == ["", "", "", "", "", "alpha", "bravo", "charlie"]


def test_Factor_pandas():
    import pandas as pd
    f1 = Factor([0, 2, 4, 2, 0], levels=["A", "B", "C", "D", "E"])
    pcat = f1.to_pandas()
    assert pcat is not None
    assert len(pcat) == len(f1)

    f2 = Factor([1, 3, 2], levels=["D", "E", "F", "G"], ordered=True)
    pcat = f2.to_pandas()
    assert pcat is not None
    assert len(pcat) == len(f2)
    assert pcat.ordered == f2.get_ordered()


def test_Factor_init_from_list():
    f1 = Factor.from_sequence(["A", "B", "A", "B", "E"])

    assert isinstance(f1, Factor)
    assert len(f1) == 5
    assert len(f1.get_levels()) == 3
