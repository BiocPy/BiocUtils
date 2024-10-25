import numpy as np
from typing import Optional, List, Union


class NamedDenseMatrix(np.matrix):
    """
    A matrix class that extends numpy.matrix to include named rows and columns.
    All numpy.matrix operations are preserved while adding the ability to reference
    and operate on the matrix using row and column names.
    """

    def __new__(cls, input_array, row_names=None, column_names=None):
        obj = np.asarray(input_array).view(cls)

        obj.row_names = list(row_names) if row_names is not None else None
        obj.column_names = list(column_names) if column_names is not None else None

        # Validate dimensions if names are provided
        if obj.row_names is not None and len(obj.row_names) != obj.shape[0]:
            raise ValueError("Number of row names must match number of rows")

        if obj.column_names is not None and len(obj.column_names) != obj.shape[1]:
            raise ValueError("Number of column names must match number of columns")

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.row_names = getattr(obj, "row_names", None)
        self.column_names = getattr(obj, "column_names", None)

    def __getitem__(self, key):
        # Handle string-based indexing when names exist
        if isinstance(key, tuple):
            row_key, col_key = key
            row_idx = self._process_key(row_key, self.row_names)
            col_idx = self._process_key(col_key, self.column_names)
            result = super().__getitem__((row_idx, col_idx))
        else:
            row_idx = self._process_key(key, self.row_names)
            result = super().__getitem__(row_idx)
            col_idx = slice(None)  # Full slice for columns when only row indexing

        # Preserve names for slice operations
        if isinstance(result, NamedDenseMatrix):
            # Handle row names
            if self.row_names is not None:
                if isinstance(row_idx, slice):
                    result.row_names = self.row_names[row_idx]
                elif isinstance(row_idx, list):
                    result.row_names = [self.row_names[i] for i in row_idx]

            # Handle column names
            if self.column_names is not None:
                if isinstance(col_idx, slice):
                    result.column_names = self.column_names[col_idx]
                elif isinstance(col_idx, list):
                    if isinstance(col_idx[0], str):
                        # If we used string names for indexing, use those directly
                        result.column_names = col_idx
                    else:
                        # If we used integer indices, get the corresponding names
                        result.column_names = [self.column_names[i] for i in col_idx]

        return result

    def _process_key(self, key, names):
        if names is None or not isinstance(key, (str, list)):
            return key

        if isinstance(key, str):
            try:
                return names.index(key)
            except ValueError:
                raise KeyError(f"Name '{key}' not found")
        elif isinstance(key, list) and all(isinstance(k, str) for k in key):
            return [names.index(k) for k in key]

        return key

    def get_value(self, row_key: Union[int, str], col_key: Union[int, str]):
        """Get a single value using row and column keys (names or indices).

        Args:
            row_key:
                Row name or index to access.

            col_key:
                Column name or index to access.

        Returns:
            A slice of the ndarray for the given row and column.
        """
        row_idx = self._process_key(row_key, self.row_names) if isinstance(row_key, str) else row_key
        col_idx = self._process_key(col_key, self.column_names) if isinstance(col_key, str) else col_key
        return self[row_idx, col_idx]

    def set_value(self, row_key, col_key, value):
        """Set a single value using row and column keys (names or indices).

        Args:
            row_key:
                Row name or index to set.

            col_key:
                Column name or index to set.

            value:
                The value to set.
        """
        row_idx = self._process_key(row_key, self.row_names) if isinstance(row_key, str) else row_key
        col_idx = self._process_key(col_key, self.column_names) if isinstance(col_key, str) else col_key
        self[row_idx, col_idx] = value

    def __str__(self):
        """Pretty print the matrix with row and column names if they exist."""
        # Calculate column widths for values
        val_widths = [[len(f"{val:.6g}") for val in row] for row in self.A]

        # Calculate name widths if names exist
        col_name_widths = (
            [len(str(name)) for name in self.column_names] if self.column_names is not None else [0] * self.shape[1]
        )
        row_name_width = (
            max(len(str(name)) for name in self.row_names)
            if self.row_names is not None
            else len(str(self.shape[0] - 1))
        )

        # Get maximum width for each column
        col_widths = [
            max(name_width, max(col_widths)) for name_width, col_widths in zip(col_name_widths, zip(*val_widths))
        ]

        # Build the string representation
        lines = []

        # Header with column names or indices
        header = " " * row_name_width + " | "
        if self.column_names is not None:
            header += " ".join(f"{name:<{width}}" for name, width in zip(self.column_names, col_widths))
        else:
            header += " ".join(f"{i:<{width}}" for i, width in enumerate(col_widths))
        lines.append(header)

        # Separator line
        separator = "-" * row_name_width + "-+-" + "-".join("-" * width for width in col_widths)
        lines.append(separator)

        # Data rows
        for i, row in enumerate(self.A):
            row_name = self.row_names[i] if self.row_names is not None else str(i)
            line = f"{str(row_name):<{row_name_width}} | "
            line += " ".join(f"{val:>{width}.6g}" for val, width in zip(row, col_widths))
            lines.append(line)

        return "\n".join(lines)

    def set_rows(self, names: Optional[List]):
        """Set row names.

        Args:
            names:
                List of names to set for rows.
                Pass None to remove row names.
        """
        if names is not None and len(names) != self.shape[0]:
            raise ValueError("Number of names must match number of rows")
        self.row_names = list(names) if names is not None else None

    def set_columns(self, names: Optional[List]):
        """Set column names.

        Args:
            names:
                List of names to set for columns.
                Pass None to remove column names.
        """
        if names is not None and len(names) != self.shape[1]:
            raise ValueError("Number of names must match number of columns")
        self.column_names = list(names) if names is not None else None

    def get_rows(self):
        """Get row names"""
        return self.row_names

    def get_columns(self):
        """Get column names."""
        return self.column_names
