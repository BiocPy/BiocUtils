from functools import singledispatch
from typing import Any

import numpy

from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def extract_column_names(x: Any) -> numpy.ndarray:
    """Access column names from 2-dimensional representations.

    Args:
        x: Any object with column names.

    Returns:
        Array of strings containing column names.
    """
    raise NotImplementedError(f"`colnames` is not supported for class: '{type(x)}'.")


if is_package_installed("pandas") is True:
    from pandas import DataFrame

    @extract_column_names.register(DataFrame)
    def _colnames_dataframe(x: DataFrame) -> list:
        return numpy.array(x.columns, dtype=str)
