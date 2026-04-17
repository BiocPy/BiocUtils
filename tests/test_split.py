import numpy
import biocutils


def test_split_basic():
    x = numpy.random.rand(10)
    f = ["B", "A"] * 5

    frag = biocutils.split(x, f)
    assert list(frag.keys()) == ["A", "B"]
    assert (frag["A"] == x[1:10:2]).all()
    assert (frag["B"] == x[0:10:2]).all()

    frag2 = biocutils.split(x, f, skip=[])
    assert list(frag.keys()) == list(frag2.keys())
    assert (frag["A"] == frag2["A"]).all()
    assert (frag["B"] == frag2["B"]).all()

    nfrag = biocutils.split(x, f, as_NamedList=True)
    assert nfrag.get_names().as_list() == ["A", "B"]


def test_split_basic_none():
    x = numpy.random.rand(15)
    f = ["A", "B", None] * 5

    frag = biocutils.split(x, f)
    assert list(frag.keys()) == ["A", "B"]
    assert (frag["A"] == x[0:15:3]).all()
    assert (frag["B"] == x[1:15:3]).all()


def test_split_Factor():
    x = numpy.random.rand(10)
    f = biocutils.Factor.from_sequence(["B", "D"] * 5, levels=["E", "D", "C", "B", "A"])

    frag = biocutils.split(x, f, drop=True)
    assert list(frag.keys()) == ["D", "B"]
    assert (frag["B"] == x[0:10:2]).all()
    assert (frag["D"] == x[1:10:2]).all()

    frag2 = biocutils.split(x, f, skip=[], drop=True)
    assert list(frag.keys()) == list(frag2.keys())
    assert (frag["B"] == frag2["B"]).all()
    assert (frag["D"] == frag2["D"]).all()

    frag = biocutils.split(x, f, drop=False)
    assert list(frag.keys()) == ["E", "D", "C", "B", "A"]


def test_split_Factor_none():
    x = numpy.random.rand(15)
    f = biocutils.Factor.from_sequence(["A", "B", None] * 5)

    frag = biocutils.split(x, f)
    assert list(frag.keys()) == ["A", "B"]
    assert (frag["A"] == x[0:15:3]).all()
    assert (frag["B"] == x[1:15:3]).all()

    frag = biocutils.split(x, f, skip=set([None, "A"]))
    assert list(frag.keys()) == ["B"]
    assert (frag["B"] == x[1:15:3]).all()
