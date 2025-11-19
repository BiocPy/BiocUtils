from functools import singledispatch
from typing import Any

import numpy

from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def extract_row_names(x: Any) -> numpy.ndarray:
    """Access row names from 2-dimensional representations.

    Args:
        x: Any object with row names.

    Returns:
        Array of strings containing row names.
    """
    raise NotImplementedError(f"`rownames` do not exist for class: '{type(x)}'.")


if is_package_installed("pandas") is True:
    from pandas import DataFrame

    @extract_row_names.register(DataFrame)
    def _rownames_dataframe(x: DataFrame) -> list:
        return numpy.array(x.index, dtype=str)
