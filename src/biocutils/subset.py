from typing import Any, Sequence

from .is_high_dimensional import is_high_dimensional
from .subset_rows import subset_rows
from .subset_sequence import subset_sequence


def subset(x: Any, indices: Sequence[int]):
    """
    Generic subset that checks if the objects are n-dimensional for n > 1 (i.e.
    has a ``shape`` property of length greater than 1); if so, it calls
    :py:func:`~biocutils.subset_rows.subset_rows` to subset them along the
    first dimension, otherwise it assumes that they are vector-like and calls
    :py:func:`~biocutils.subset_sequence.subset_sequence` instead.

    Args:
        x: Object to be subsetted.

    Returns:
        The subsetted object, typically the same type as ``x``.
    """
    if is_high_dimensional(x):
        return subset_rows(x, indices)
    else:
        return subset_sequence(x, indices)
