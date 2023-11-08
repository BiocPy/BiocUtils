from biocutils import extract_column_names
import pandas
import numpy


def test_pandas_column_names():
    p = pandas.DataFrame({ "A": [1,2,3,4,5], "B": ["a", "b", "c", "d", "e" ]})
    assert (extract_column_names(p) == numpy.array(["A", "B"])).all()
