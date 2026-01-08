import biocutils


def test_duplicated_basic():
    assert list(biocutils.duplicated([1,2,1,2,3,2])) == [False, False, True, True, False, True] 
    assert list(biocutils.duplicated([1,2,1,2,3,2], from_last=True)) == [True, True, False, True, False, False] 
    assert list(biocutils.duplicated([1,2,None,None,3,2,3])) == [False, False, False, True, False, True, True]
    assert list(biocutils.duplicated([1,2,None,None,3,2,3], incomparables=set([None]))) == [False, False, False, False, False, True, True]


def test_duplicated_Factor():
    assert list(biocutils.duplicated(biocutils.Factor.from_sequence([1,2,1,2,3,2]))) == [False, False, True, True, False, True] 
    assert list(biocutils.duplicated(biocutils.Factor.from_sequence([1,2,1,2,3,2]), from_last=True)) == [True, True, False, True, False, False] 
    assert list(biocutils.duplicated(biocutils.Factor.from_sequence([1,2,None,None,3,2,3]))) == [False, False, False, True, False, True, True]
    assert list(biocutils.duplicated(biocutils.Factor.from_sequence([1,2,None,None,3,2,3]), incomparables=set([None]))) == [False, False, False, False, False, True, True]


def test_unique():
    assert biocutils.unique([1,2,1,2,3,2]) == [1,2,3]
    assert biocutils.unique([1,2,1,2,3,2], from_last=True) == [1,3,2]
    assert biocutils.unique([1,2,None,None,3,2]) == [1,2,None,3]
    assert biocutils.unique([1,2,None,None,3,2], incomparables=set([None])) == [1,2,None,None,3]
