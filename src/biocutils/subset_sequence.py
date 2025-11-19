from functools import singledispatch
from typing import Any, Sequence, Union


@singledispatch
def subset_sequence(x: Any, indices: Sequence[int]) -> Any:
    """Subset a sequence-like object by indices.

    Subset ``x`` by ``indices`` to obtain a new object. The default method
    attempts to use ``x``'s ``__getitem__`` method.

    Args:
        x: Any object that supports ``__getitem__`` with an integer sequence.
        indices: Sequence of non-negative integers specifying the positions of
            interest. All indices should be less than ``len(x)``.

    Returns:
        The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns.
    """
    return x[indices]


@subset_sequence.register
def _subset_sequence_list(x: list, indices: Sequence[int]) -> list:
    """Subset a list by indices.

    Args:
        x: List to subset.
        indices: Sequence of non-negative integers specifying positions.

    Returns:
        A new list containing the specified elements.
    """
    return type(x)(x[i] for i in indices)


@subset_sequence.register
def _subset_sequence_range(x: range, indices: Sequence[int]) -> Union[list, range]:
    """Subset a range by indices.

    Args:
        x: Range object to subset.
        indices: Sequence of non-negative integers or a range object.

    Returns:
        A range if indices is a range, otherwise a list.
    """
    if isinstance(indices, range):
        # We can just assume that all 'indices' are in [0, len(x)),
        # so no need to handle out-of-range indices.
        return range(x.start + x.step * indices.start, x.start + x.step * indices.stop, x.step * indices.step)
    else:
        return [x[i] for i in indices]


@subset_sequence.register
def _subset_sequence_tuple(x: tuple, indices: Sequence[int]) -> tuple:
    """Subset a tuple by indices.

    Args:
        x: Tuple to subset.
        indices: Sequence of non-negative integers specifying positions.

    Returns:
        A new tuple containing the specified elements.
    """
    return tuple(x[i] for i in indices)
