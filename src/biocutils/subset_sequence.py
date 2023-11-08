from typing import Any, Sequence, Union
from functools import singledispatch
import numpy


@singledispatch
def subset_sequence(x: Any, indices: Sequence) -> Any:
    """
    Subset ``x`` by ``indices`` to obtain a new object with the desired
    subset of elements. This attempts to use ``x``'s ``__getitem__`` method.

    Args:
        x:
            Any object that supports ``__getitem__`` with an integer sequence.

        indices:
            Sequence of non-negative integers specifying the integers of interest.

    Returns:
        The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns.
    """
    return x[indices]


@subset_sequence.register
def _subset_sequence_list(x: list, indices: Sequence) -> list:
    return [x[i] for i in indices]
