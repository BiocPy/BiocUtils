import numpy as np
import pandas as pd
from biocutils import combine_rows
from scipy import sparse as sp

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_combine_rows_dense():
    num_cols = 20
    x = np.ones(shape=(10, num_cols))
    y = np.random.rand(5, num_cols)

    z = combine_rows(x, y)

    assert isinstance(z, np.ndarray)
    assert z.shape == (15, 20)


def test_combine_rows_masked():
    num_cols = 20
    x = np.ones(shape=(10, num_cols))
    y0 = np.zeros((5, num_cols))
    y = np.ma.array(y0, mask=True)

    z = combine_rows(x, y)
    expected = np.concatenate([x, y0]) == 0
    assert (z.mask == expected).all()
    assert z.shape == (15, 20)


def test_combine_rows_sparse():
    num_cols = 20

    x = sp.random(10, num_cols)
    y = sp.identity(num_cols)

    z = combine_rows(x, y)

    assert isinstance(z, sp.spmatrix)
    assert z.shape == (30, 20)


def test_combine_rows_mixed():
    num_cols = 20
    x = np.ones(shape=(10, num_cols))
    y = sp.identity(num_cols)

    z = combine_rows(x, y)

    assert isinstance(z, np.ndarray)
    assert z.shape == (30, 20)


def test_pandas_dataframe():
    df1 = pd.DataFrame([["a", 1], ["b", 2]], columns=["letter", "number"])

    df2 = pd.DataFrame(
        [["c", 3, "cat"], ["d", 4, "dog"]], columns=["letter", "number", "animal"]
    )

    z = combine_rows(df1, df2)
    assert isinstance(z, pd.DataFrame)


def test_combine_rows_ndim():
    num_cols = 20
    x = np.ones(shape=(20, num_cols, 20))
    y = np.ones(shape=(10, num_cols, num_cols))

    z = combine_rows(x, y, y)

    assert isinstance(z, np.ndarray)
    assert z.shape == (40, 20, 20)
