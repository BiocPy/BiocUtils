from typing import Any

from .combine_rows import combine_rows
from .combine_sequences import combine_sequences


def combine(*x: Any):
    """
    Generic combine that checks if the objects are n-dimensional for n > 1
    (i.e. has a ``shape`` property of length greater than 1); if so, it calls
    :py:func:`~biocgenerics.combine_rows.combine_rows` to combine them by
    the first dimension, otherwise it assumes that they are vector-like and
    calls :py:func:`~biocgenerics.combine_seqs.combine_seqs` instead.

    Args:
        x: Objects to combine.

    Returns:
        A combined object, typically the same type as the first element in ``x``.
    """
    if hasattr(x[0], "shape") and len(x[0].shape) > 1:
        return combine_rows(*x)
    else:
        return combine_sequences(*x)
