from typing import List, Optional, Tuple, Union, Dict

import numpy as np
import scipy.sparse as sp
from scipy.sparse import spmatrix


class NamedSparseMatrix:
    """
    A wrapper class for scipy sparse matrices that adds optional row and column naming
    capabilities while preserving all sparse matrix operations and format-specific optimizations.
    """

    def __init__(
        self,
        matrix: spmatrix,
        row_names: Optional[List[str]] = None,
        column_names: Optional[List[str]] = None,
    ):
        """
        Initialize with a scipy sparse matrix and optional row/column names.

        Args:
            matrix:
                Any scipy sparse matrix.

            row_names:
                List of row names. If None, will use indices.

            column_names:
                List of column names. If None, will use indices.
        """
        self._matrix = matrix
        self.row_names = list(row_names) if row_names is not None else None
        self.column_names = list(column_names) if column_names is not None else None

        # Validate dimensions if names are provided
        if self.row_names is not None and len(self.row_names) != matrix.shape[0]:
            raise ValueError("Number of row names must match number of rows")

        if self.column_names is not None and len(self.column_names) != matrix.shape[1]:
            raise ValueError("Number of column names must match number of columns")

        self._row_to_idx: Dict[str, int] = (
            {name: idx for idx, name in enumerate(self.row_names)}
            if self.row_names is not None
            else {}
        )
        self._col_to_idx: Dict[str, int] = (
            {name: idx for idx, name in enumerate(self.column_names)}
            if self.column_names is not None
            else {}
        )

    @property
    def shape(self) -> Tuple[int, int]:
        return self._matrix.shape

    @property
    def nnz(self) -> int:
        return self._matrix.nnz

    @property
    def dtype(self):
        return self._matrix.dtype

    def _process_key(self, key, name_to_idx):
        """Convert string keys to integer indices when names exist."""
        if not name_to_idx or not isinstance(key, (str, list)):
            return key

        if isinstance(key, str):
            return name_to_idx[key]
        elif isinstance(key, list) and all(isinstance(k, str) for k in key):
            return [name_to_idx[k] for k in key]

        return key

    def __getitem__(self, key):
        """Support both integer and name-based indexing."""
        if isinstance(key, tuple):
            row_key, col_key = key
            row_idx = self._process_key(row_key, self._row_to_idx)
            col_idx = self._process_key(col_key, self._col_to_idx)
            result = self._matrix[row_idx, col_idx]
        else:
            row_idx = self._process_key(key, self._row_to_idx)
            result = self._matrix[row_idx]

        # If result is a matrix, wrap it with names
        if sp.issparse(result):
            # Get the new names based on the indices
            new_row_names = None
            new_column_names = None

            if self.row_names is not None:
                if isinstance(row_idx, slice):
                    new_row_names = self.row_names[row_idx]
                elif isinstance(row_idx, list):
                    new_row_names = [self.row_names[i] for i in row_idx]

            if self.column_names is not None:
                if isinstance(col_idx, slice):
                    new_column_names = self.column_names[col_idx]
                elif isinstance(col_idx, list):
                    new_column_names = [self.column_names[i] for i in col_idx]

            return NamedSparseMatrix(result, new_row_names, new_column_names)

        return result

    def get_value(self, row_key, col_key):
        """Get a single value using row and column keys (names or indices).

        Args:
            row_key:
                Row name or index to access.

            col_key:
                Column name or index to access.

        Returns:
            A slice of the ndarray for the given row and column.
        """
        row_idx = (
            self._process_key(row_key, self._row_to_idx)
            if isinstance(row_key, str)
            else row_key
        )
        col_idx = (
            self._process_key(col_key, self._col_to_idx)
            if isinstance(col_key, str)
            else col_key
        )
        return self._matrix[row_idx, col_idx]

    def set_value(self, row_key, col_key, value):
        """Set a single value using row and column keys (names or indices).

        Args:
            row_key:
                Row name or index to set.

            col_key:
                Column name or index to set.
        """
        row_idx = (
            self._process_key(row_key, self._row_to_idx)
            if isinstance(row_key, str)
            else row_key
        )
        col_idx = (
            self._process_key(col_key, self._col_to_idx)
            if isinstance(col_key, str)
            else col_key
        )
        self._matrix[row_idx, col_idx] = value

    def set_rows(self, names: Optional[List[str]]):
        """Set row names.

        Args:
            names:
                List of names to set for columns.
                Pass None to remove column names.
        """
        if names is not None and len(names) != self.shape[0]:
            raise ValueError("Number of names must match number of rows")

        self.row_names = list(names) if names is not None else None
        self._row_to_idx = (
            {name: idx for idx, name in enumerate(self.row_names)}
            if names is not None
            else {}
        )

    def set_columns(self, names: Optional[List[str]]):
        """Set column names.

        Args:
            names:
                List of names to set for columns.
                Pass None to remove column names.
        """
        if names is not None and len(names) != self.shape[1]:
            raise ValueError("Number of names must match number of columns")

        self.column_names = list(names) if names is not None else None
        self._col_to_idx = (
            {name: idx for idx, name in enumerate(self.column_names)}
            if names is not None
            else {}
        )

    def __str__(self):
        """Pretty print the sparse matrix with row and column names if they exist."""
        # Convert to dense for small matrices, otherwise show summary
        if self.shape[0] * self.shape[1] < 1000:  # arbitrary threshold
            dense = self._matrix.todense()

            # Calculate column widths
            val_widths = [[len(f"{val:.6g}") for val in row] for row in dense.A]

            # Calculate name widths if names exist
            col_name_widths = (
                [len(str(name)) for name in self.column_names]
                if self.column_names is not None
                else [len(str(i)) for i in range(self.shape[1])]
            )
            row_name_width = (
                max(len(str(name)) for name in self.row_names)
                if self.row_names is not None
                else len(str(self.shape[0] - 1))
            )

            # Get maximum width for each column
            col_widths = [
                max(name_width, max(col_widths))
                for name_width, col_widths in zip(col_name_widths, zip(*val_widths))
            ]

            # Build the string representation
            lines = []

            # Header with column names or indices
            header = " " * row_name_width + " | "
            names = (
                self.column_names
                if self.column_names is not None
                else range(self.shape[1])
            )
            header += " ".join(
                f"{name:<{width}}" for name, width in zip(names, col_widths)
            )
            lines.append(header)

            # Separator line
            separator = (
                "-" * row_name_width
                + "-+-"
                + "-".join("-" * width for width in col_widths)
            )
            lines.append(separator)

            # Data rows
            for i, row in enumerate(dense.A):
                row_name = self.row_names[i] if self.row_names is not None else str(i)
                line = f"{str(row_name):<{row_name_width}} | "
                line += " ".join(
                    f"{val:>{width}.6g}" for val, width in zip(row, col_widths)
                )
                lines.append(line)

            return "\n".join(lines)
        else:
            return (
                f"<NamedSparseMatrix: shape={self.shape}, nnz={self.nnz}, "
                f"format='{self._matrix.format}', dtype={self.dtype}>"
            )

    def __repr__(self):
        return self.__str__()

    # Delegate all common matrix operations to the underlying sparse matrix
    def tocsr(self):
        return NamedSparseMatrix(
            self._matrix.tocsr(), self.row_names, self.column_names
        )

    def tocsc(self):
        return NamedSparseMatrix(
            self._matrix.tocsc(), self.row_names, self.column_names
        )

    def tocoo(self):
        return NamedSparseMatrix(
            self._matrix.tocoo(), self.row_names, self.column_names
        )

    def todense(self):
        return self._matrix.todense()

    def toarray(self):
        return self._matrix.toarray()

    def transpose(self):
        return NamedSparseMatrix(
            self._matrix.transpose(), self.column_names, self.row_names
        )

    def __add__(self, other):
        if isinstance(other, NamedSparseMatrix):
            other = other._matrix
        return NamedSparseMatrix(
            self._matrix + other, self.row_names, self.column_names
        )

    def __mul__(self, other):
        if isinstance(other, NamedSparseMatrix):
            other = other._matrix

        result = self._matrix * other
        if sp.issparse(result):
            return NamedSparseMatrix(result, self.row_names, self.column_names)
        return result

    def __rmul__(self, other):
        result = other * self._matrix
        if sp.issparse(result):
            return NamedSparseMatrix(result, self.row_names, self.column_names)
        return result

    @classmethod
    def from_coo(cls, row, col, data, shape=None, row_names=None, column_names=None):
        """Create a NamedSparseMatrix from COO format data."""
        matrix = sp.coo_matrix((data, (row, col)), shape=shape)
        return cls(matrix, row_names, column_names)
