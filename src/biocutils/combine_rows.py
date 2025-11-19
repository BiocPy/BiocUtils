from functools import singledispatch
from typing import Any
from warnings import warn

import numpy

from ._utils_combine import (
    _check_array_dimensions,
    _coerce_sparse_array,
    _coerce_sparse_matrix,
)
from .convert_to_dense import convert_to_dense
from .is_list_of_type import is_list_of_type
from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def combine_rows(*x: Any):
    """Combine n-dimensional objects along their first dimension.

    If all elements are :py:class:`~numpy.ndarray`, we combine them using
    numpy's :py:func:`~numpy.concatenate`.

    If all elements are either :py:class:`~scipy.sparse.spmatrix` or
    :py:class:`~scipy.sparse.sparray`, these objects are combined using scipy's
    :py:class:`~scipy.sparse.vstack`.

    If all elements are :py:class:`~pandas.DataFrame` objects, they are
    combined using :py:func:`~pandas.concat` along the first axis.

    Args:
        x:
            One or more n-dimensional objects to combine. All elements of x
            are expected to be the same class.

    Returns:
        Combined object, typically the same type as the first entry of ``x``.
    """
    raise NotImplementedError(
        "no `combine_rows` method implemented for '" + type(x[0]).__name__ + "' objects"
    )


@combine_rows.register(numpy.ndarray)
def _combine_rows_dense_arrays(*x: numpy.ndarray):
    _check_array_dimensions(x, active=0)
    x = [convert_to_dense(y) for y in x]
    for y in x:
        if numpy.ma.is_masked(y):
            return numpy.ma.concatenate(x)
    return numpy.concatenate(x)


if is_package_installed("scipy"):
    import scipy.sparse as sp

    def _combine_rows_sparse_matrices(*x):
        _check_array_dimensions(x, 0)
        if is_list_of_type(x, sp.spmatrix):
            combined = sp.vstack(x)
            return _coerce_sparse_matrix(x[0], combined, sp)

        warn("not all elements are SciPy sparse matrices")
        x = [convert_to_dense(y) for y in x]
        return numpy.concatenate(x)

    try:
        combine_rows.register(sp.sparray, _combine_rows_sparse_arrays)
    except Exception:
        pass

    def _combine_rows_sparse_arrays(*x):
        _check_array_dimensions(x, 0)
        if is_list_of_type(x, sp.sparray):
            combined = sp.vstack(x)
            return _coerce_sparse_array(x[0], combined, sp)

        warn("not all elements are SciPy sparse arrays")
        x = [convert_to_dense(y) for y in x]
        return numpy.concatenate(x)

    try:
        combine_rows.register(sp.spmatrix, _combine_rows_sparse_matrices)
    except Exception:
        pass


if is_package_installed("pandas"):
    from pandas import DataFrame, concat

    @combine_rows.register(DataFrame)
    def _combine_rows_pandas_dataframe(*x):
        return concat(x, axis=0)
