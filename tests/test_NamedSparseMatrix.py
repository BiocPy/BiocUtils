import pytest
import numpy as np
import scipy.sparse as sp

from biocutils import NamedSparseMatrix


def sparse_data():
    """Create sample sparse matrix data."""
    return sp.csr_matrix([[1, 0, 2], [0, 3, 0], [4, 0, 5]])


def test_initialization():
    """Test different initialization scenarios."""
    # Basic initialization
    mat = NamedSparseMatrix(sparse_data())
    assert mat.shape == (3, 3)
    assert mat.row_names is None
    assert mat.column_names is None

    # With names
    mat = NamedSparseMatrix(
        sparse_data(), row_names=["r1", "r2", "r3"], column_names=["c1", "c2", "c3"]
    )
    assert mat.row_names == ["r1", "r2", "r3"]
    assert mat.column_names == ["c1", "c2", "c3"]

    # Mixed naming
    mat = NamedSparseMatrix(sparse_data(), row_names=["r1", "r2", "r3"])
    assert mat.row_names == ["r1", "r2", "r3"]
    assert mat.column_names is None

    # Invalid dimensions
    with pytest.raises(ValueError):
        NamedSparseMatrix(sparse_data(), row_names=["r1"])
    with pytest.raises(ValueError):
        NamedSparseMatrix(sparse_data(), column_names=["c1"])


def test_format_conversion():
    """Test conversion between sparse formats."""
    mat = NamedSparseMatrix(
        sparse_data(), row_names=["r1", "r2", "r3"], column_names=["c1", "c2", "c3"]
    )

    # Test CSR conversion
    csr_mat = mat.tocsr()
    assert isinstance(csr_mat, NamedSparseMatrix)
    assert csr_mat.row_names == mat.row_names
    assert csr_mat.column_names == mat.column_names

    # Test CSC conversion
    csc_mat = mat.tocsc()
    assert isinstance(csc_mat, NamedSparseMatrix)
    assert csc_mat.row_names == mat.row_names
    assert csc_mat.column_names == mat.column_names

    # Test COO conversion
    coo_mat = mat.tocoo()
    assert isinstance(coo_mat, NamedSparseMatrix)
    assert coo_mat.row_names == mat.row_names
    assert coo_mat.column_names == mat.column_names


def test_indexing():
    """Test different indexing methods."""
    mat = NamedSparseMatrix(
        sparse_data(), row_names=["r1", "r2", "r3"], column_names=["c1", "c2", "c3"]
    )

    # Integer indexing
    assert mat[0, 0] == 1
    assert mat[1, 1] == 3

    # Name indexing
    assert mat["r1", "c1"] == 1
    assert mat["r2", "c2"] == 3

    # Mixed indexing
    assert mat[0, "c2"] == 0
    assert mat["r2", 1] == 3

    # Invalid names
    with pytest.raises(KeyError):
        mat["invalid", "c1"]

    # Slicing
    sub_mat = mat[0:2, ["c1", "c2"]]
    assert isinstance(sub_mat, NamedSparseMatrix)
    assert sub_mat.shape == (2, 2)
    assert sub_mat.row_names == ["r1", "r2"]
    assert sub_mat.column_names == ["c1", "c2"]


def test_operations():
    """Test mathematical operations."""
    mat = NamedSparseMatrix(
        sparse_data(), row_names=["r1", "r2", "r3"], column_names=["c1", "c2", "c3"]
    )

    # Multiplication by scalar
    result = mat * 2
    assert isinstance(result, NamedSparseMatrix)
    assert result.row_names == mat.row_names
    assert result.column_names == mat.column_names
    assert not np.allclose(result._matrix.data, mat._matrix.data)

    # Matrix multiplication
    result = mat * mat
    assert isinstance(result, NamedSparseMatrix)
    assert result.row_names == mat.row_names
    assert result.column_names == mat.column_names

    # Addition
    result = mat + mat
    assert isinstance(result, NamedSparseMatrix)
    assert result.row_names == mat.row_names
    assert result.column_names == mat.column_names


def test_get_set_value():
    """Test getting and setting values."""
    mat = NamedSparseMatrix(
        sparse_data(), row_names=["r1", "r2", "r3"], column_names=["c1", "c2", "c3"]
    )

    # Get values
    assert mat.get_value("r1", "c1") == 1
    assert mat.get_value("r2", "c2") == 3
    assert mat.get_value("r1", "c2") == 0

    # Set values
    mat.set_value("r1", "c2", 7)
    assert mat.get_value("r1", "c2") == 7

    # Set using indices
    mat.set_value(0, 1, 8)
    assert mat.get_value("r1", "c2") == 8


def test_rename():
    """Test renaming functionality."""
    mat = NamedSparseMatrix(sparse_data())

    # Add names
    mat.set_rows(["r1", "r2", "r3"])
    mat.set_columns(["c1", "c2", "c3"])
    assert mat.row_names == ["r1", "r2", "r3"]
    assert mat.column_names == ["c1", "c2", "c3"]

    # Remove names
    mat.set_rows(None)
    mat.set_columns(None)
    assert mat.row_names is None
    assert mat.column_names is None

    # Invalid renaming
    with pytest.raises(ValueError):
        mat.set_rows(["single"])
    with pytest.raises(ValueError):
        mat.set_columns(["single"])
