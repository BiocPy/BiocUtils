from typing import Any, Sequence, Union
from functools import singledispatch
from copy import deepcopy
import numpy


@singledispatch
def assign_rows(x: Any, indices: Sequence[int], replacement: Any) -> Any:
    """
    Assign ``replacement`` values to a copy of ``x`` at the rows specified by
    ``indices``. This defaults to creating a deep copy of ``x`` and then
    assigning ``replacement`` to the first dimension of the copy.

    Args:
        x:
            Any high-dimensional object.

        indices: 
            Sequence of non-negative integers specifying rows of ``x``.

        replacement:
            Replacement values to be assigned to ``x``. This should have the
            same number of rows as the length of ``indices``. Typically
            ``replacement`` will have the same dimensionality as ``x``.

    Returns:
        A copy of ``x`` with the rows replaced at ``indices``.
    """
    output = deepcopy(x)
    tmp = [slice(None)] * len(x.shape)
    tmp[0] = indices 
    output[(*tmp,)] = replacement
    return output


@assign_rows.register
def _assign_rows_numpy(x: numpy.ndarray, indices: Sequence[int], replacement: Any) -> numpy.ndarray:
    tmp = [slice(None)] * len(x.shape)
    tmp[0] = indices 
    output = numpy.copy(x)
    output[(*tmp,)] = replacement
    return output
