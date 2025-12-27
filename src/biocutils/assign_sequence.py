from copy import deepcopy
from functools import singledispatch
from typing import Any, Sequence, Union

import numpy


@singledispatch
def assign_sequence(x: Any, indices: Sequence[int], replacement: Any) -> Any:
    """
    Assign ``replacement`` values to a copy of ``x`` at the specified ``indices``.
    This defaults to creating a deep copy of ``x`` and then iterating through
    ``indices`` to assign the values of ``replacement``.

    Args:
        x:
            Any sequence-like object that can be assigned.

        indices:
            Sequence of non-negative integers specifying positions on ``x``.

        replacement:
            Replacement values to be assigned to ``x``. This should have the
            same length as ``indices``.

    Returns:
        A copy of ``x`` with the replacement values.
    """
    output = deepcopy(x)
    for i, j in enumerate(indices):
        output[j] = replacement[i]
    return output


@assign_sequence.register
def _assign_sequence_list(x: list, indices: Sequence[int], replacement: Any) -> list:
    output = x.copy()
    for i, j in enumerate(indices):
        output[j] = replacement[i]
    return output


@assign_sequence.register
def _assign_sequence_numpy(x: numpy.ndarray, indices: Sequence[int], replacement: Any) -> numpy.ndarray:
    output = numpy.copy(x)
    output[indices] = replacement
    return output


@assign_sequence.register
def _assign_sequence_range(x: range, indices: Sequence[int], replacement: Any) -> Union[range, list]:
    if (
        isinstance(replacement, range)
        and isinstance(indices, range)
        and x[slice(indices.start, indices.stop, indices.step)] == replacement
    ):
        return x

    output = list(x)
    for i, j in enumerate(indices):
        output[j] = replacement[i]
    return output
