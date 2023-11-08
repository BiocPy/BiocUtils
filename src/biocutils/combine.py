from typing import Any

from .combine_rows import combine_rows
from .combine_sequences import combine_sequences
from .is_high_dimensional import is_high_dimensional


def combine(*x: Any):
    """
    Generic combine that checks if the objects are n-dimensional for n > 1
    (i.e. has a ``shape`` property of length greater than 1); if so, it calls
    :py:func:`~biocutils.combine_rows.combine_rows` to combine them by the
    first dimension, otherwise it assumes that they are vector-like and calls
    :py:func:`~biocutils.combine_sequences.combine_sequences` instead.

    Args:
        x: Objects to combine.

    Returns:
        A combined object, typically the same type as the first element in ``x``.
    """
    has_1d = False
    has_nd = False
    for y in x:
        if is_high_dimensional(y):
            has_nd = True
        else:
            has_1d = True

    if has_nd and has_1d:
        raise ValueError("cannot mix 1-dimensional and higher-dimensional objects in `combine`")
    if has_nd:
        return combine_rows(*x)
    else:
        return combine_sequences(*x)
