import numpy
import biocutils


def test_split_basic():
    x = numpy.random.rand(10)
    f = ["B", "A"] * 5
    frag = biocutils.split(x, f)
    assert list(frag.keys()) == ["A", "B"]
    assert (frag["A"] == x[1:10:2]).all()
    assert (frag["B"] == x[0:10:2]).all()

    frag = biocutils.split(x, f, as_NamedList=True)
    assert frag.get_names().as_list() == ["A", "B"]


def test_split_Factor():
    x = numpy.random.rand(10)
    f = biocutils.Factor.from_sequence(["B", "D"] * 5, levels=["E", "D", "C", "B", "A"])
    frag = biocutils.split(x, f, drop=True)
    assert list(frag.keys()) == ["D", "B"]
    assert (frag["B"] == x[0:10:2]).all()
    assert (frag["D"] == x[1:10:2]).all()

    frag = biocutils.split(x, f, drop=False)
    assert list(frag.keys()) == ["E", "D", "C", "B", "A"]
