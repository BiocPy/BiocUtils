from functools import singledispatch
from typing import Any

import numpy

from .package_utils import is_package_installed


@singledispatch
def convert_to_dense(x: Any) -> numpy.ndarray:
    """
    Convert something to a NumPy dense array of the same shape.
    This is typically used a fallback for the various combining
    methods when there are lots of different array types that
    ``numpy.concatenate`` doesn't understand.

    Args:
        x:
            Some array-like object to be stored as a NumPy array.

    Returns:
        A NumPy array.
    """
    return numpy.array(x)


@convert_to_dense.register
def _convert_to_dense_numpy(x: numpy.ndarray) -> numpy.ndarray:
    return x


if is_package_installed("scipy"):
    import scipy.sparse as sp

    def _convert_sparse_to_dense(x):
        return x.todense()

    try:
        convert_to_dense.register(sp.spmatrix, _convert_sparse_to_dense)
    except Exception:
        pass

    try:
        convert_to_dense.register(sp.sparray, _convert_sparse_to_dense)
    except Exception:
        pass
