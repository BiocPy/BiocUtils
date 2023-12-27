from functools import singledispatch
from typing import Any

from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def relaxed_combine_columns(*x: Any):
    """Combine n-dimensional objects along the second dimension.

    Args:
        x:
            n-dimensional objects to combine. All elements of x are expected
            to be the same class.

    Returns:
        Combined object, typically the same type as the first entry of ``x``
    """
    raise NotImplementedError(
        "no `combine_columns` method implemented for '"
        + type(x[0]).__name__
        + "' objects."
    )


if is_package_installed("pandas") is True:
    from pandas import DataFrame, concat

    @relaxed_combine_columns.register(DataFrame)
    def _relaxed_combine_columns_pandas_dataframe(*x):
        return concat(x, axis=1)
