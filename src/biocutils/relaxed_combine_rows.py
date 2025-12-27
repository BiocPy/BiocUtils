from functools import singledispatch
from typing import Any

from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def relaxed_combine_rows(*x: Any):
    """Combine n-dimensional objects along their first dimension.

    Args:
        x:
            One or more n-dimensional objects to combine. All elements of x
            are expected to be the same class.

    Returns:
        Combined object, typically the same type as the first entry of ``x``.
    """
    raise NotImplementedError("no `combine_rows` method implemented for '" + type(x[0]).__name__ + "' objects.")


if is_package_installed("pandas"):
    from pandas import DataFrame, concat

    @relaxed_combine_rows.register(DataFrame)
    def _relaxed_combine_rows_pandas_dataframe(*x):
        return concat(x, axis=0)
