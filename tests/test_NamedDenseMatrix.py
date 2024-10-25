import pytest
import numpy as np
import scipy.sparse as sp

from biocutils import NamedDenseMatrix, NamedSparseMatrix


def test_initialization():
    """Test different initialization scenarios."""
    # Basic initialization
    data = [[1, 2], [3, 4]]
    mat = NamedDenseMatrix(data)
    assert mat.shape == (2, 2)
    assert mat.row_names is None
    assert mat.column_names is None

    # With names
    mat = NamedDenseMatrix(data, row_names=["r1", "r2"], column_names=["c1", "c2"])
    assert mat.row_names == ["r1", "r2"]
    assert mat.column_names == ["c1", "c2"]

    # Mixed naming
    mat = NamedDenseMatrix(data, row_names=["r1", "r2"])
    assert mat.row_names == ["r1", "r2"]
    assert mat.column_names is None

    # Invalid dimensions
    with pytest.raises(ValueError):
        NamedDenseMatrix(data, row_names=["r1"])
    with pytest.raises(ValueError):
        NamedDenseMatrix(data, column_names=["c1"])


def test_indexing():
    """Test different indexing methods."""
    data = [[1, 2, 3], [4, 5, 6]]
    mat = NamedDenseMatrix(data, row_names=["r1", "r2"], column_names=["c1", "c2", "c3"])

    # Integer indexing
    assert mat[0, 0] == 1
    assert mat[1, 2] == 6

    # Name indexing
    assert mat["r1", "c1"] == 1
    assert mat["r2", "c3"] == 6

    # Mixed indexing
    assert mat[0, "c2"] == 2
    assert mat["r2", 1] == 5

    # Invalid names
    with pytest.raises(KeyError):
        mat["invalid", "c1"]

    # Slicing
    sub_mat = mat[0:2, ["c1", "c2"]]
    # assert isinstance(sub_mat, NamedDenseMatrix)
    assert sub_mat.shape == (2, 2)
    assert sub_mat.row_names == ["r1", "r2"]
    assert sub_mat.column_names == ["c1", "c2"]


# def test_operations():
#     """Test mathematical operations."""
#     data = [[1, 2], [3, 4]]
#     mat = NamedDenseMatrix(data, row_names=["r1", "r2"], column_names=["c1", "c2"])

#     # Multiplication
#     result = mat * 2
#     assert isinstance(result, NamedDenseMatrix)
#     assert result.row_names == mat.row_names
#     assert result.column_names == mat.column_names
#     assert np.array_equal(result.A, np.array(data) * 2)

#     # Matrix multiplication
#     result = mat @ mat
#     assert isinstance(result, NamedDenseMatrix)
#     assert result.row_names == mat.row_names
#     assert result.column_names == mat.column_names

#     # Addition
#     result = mat + mat
#     assert isinstance(result, NamedDenseMatrix)
#     assert result.row_names == mat.row_names
#     assert result.column_names == mat.column_names
#     assert np.array_equal(result.A, np.array(data) * 2)


# def test_rename():
#     """Test renaming functionality."""
#     mat = NamedDenseMatrix([[1, 2], [3, 4]])

#     # Add names
#     mat.set_rows(["r1", "r2"])
#     mat.set_columns(["c1", "c2"])
#     assert mat.row_names == ["r1", "r2"]
#     assert mat.column_names == ["c1", "c2"]

#     # Remove names
#     mat.set_rows(None)
#     mat.set_columns(None)
#     assert mat.row_names is None
#     assert mat.column_names is None

#     # Invalid renaming
#     with pytest.raises(ValueError):
#         mat.set_rows(["single"])
#     with pytest.raises(ValueError):
#         mat.set_columns(["single"])
