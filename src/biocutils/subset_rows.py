from functools import singledispatch
from typing import Any, Sequence

import numpy

from .package_utils import is_package_installed


@singledispatch
def subset_rows(x: Any, indices: Sequence[int]) -> Any:
    """Subset a high-dimensional object by indices on the first dimension.

    Subset ``x`` by ``indices`` on the first dimension. The default
    method attempts to use ``x``'s ``__getitem__`` method.

    Args:
        x: Any high-dimensional object.
        indices: Sequence of non-negative integers specifying the rows of interest.

    Returns:
        The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns.
    """
    tmp = [slice(None)] * len(x.shape)
    tmp[0] = indices
    return x[(*tmp,)]


@subset_rows.register
def _subset_rows_numpy(x: numpy.ndarray, indices: Sequence[int]) -> numpy.ndarray:
    """Subset a NumPy array by row indices.

    Args:
        x: NumPy array to subset.
        indices: Sequence of non-negative integers specifying rows.

    Returns:
        Subsetted NumPy array.
    """
    tmp = [slice(None)] * len(x.shape)
    tmp[0] = indices
    return x[(*tmp,)]


if is_package_installed("pandas"):
    from pandas import DataFrame

    @subset_rows.register(DataFrame)
    def _subset_rows_dataframe(x: DataFrame, indices: Sequence[int]) -> DataFrame:
        """Subset a pandas DataFrame by row indices.

        Args:
            x: DataFrame to subset.
            indices: Sequence of non-negative integers specifying rows.

        Returns:
            Subsetted DataFrame.
        """
        return x.iloc[indices, :]
