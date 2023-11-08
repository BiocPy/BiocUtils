from biocutils import extract_row_names
import pandas
import numpy


def test_pandas_row_names():
    p = pandas.DataFrame({ "A": [1,2,3,4,5] })
    rn = ["a", "b", "c", "d", "e" ]
    p.index = rn
    assert (extract_row_names(p) == numpy.array(rn)).all()
