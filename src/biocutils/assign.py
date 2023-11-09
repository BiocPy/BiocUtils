from typing import Any, Sequence

from .assign_rows import assign_rows
from .assign_sequence import assign_sequence
from .is_high_dimensional import is_high_dimensional


def assign(x: Any, indices: Sequence[int], replacement: Any) -> Any:
    """
    Generic assign that checks if the objects are n-dimensional for n > 1 (i.e.
    has a ``shape`` property of length greater than 1); if so, it calls
    :py:func:`~biocutils.assign_rows.assign_rows` to assign them along the
    first dimension, otherwise it assumes that they are vector-like and calls
    :py:func:`~biocutils.assign_sequence.assign_sequence` instead.

    Args:
        x: Object to be assignted.

    Returns:
        The object after assignment, typically the same type as ``x``.
    """
    if is_high_dimensional(x):
        return assign_rows(x, indices, replacement)
    else:
        return assign_sequence(x, indices, replacement)
