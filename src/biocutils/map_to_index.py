from typing import Literal, Sequence

from .is_missing_scalar import is_missing_scalar


DUPLICATE_METHOD = Literal["first", "last"]


def map_to_index(x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> dict:
    """
    Create a dictionary to map values of a sequence to positional indices.

    Args:
        x:
            Sequence of hashable values. We ignore missing values defined by 
            :py:meth:`~biocutils.is_missing_scalar.is_missing_scalar`.

        duplicate_method:
            Whether to consider the first or last occurrence of a duplicated
            value in ``x``.

    Returns:
        dict: Dictionary that maps values of ``x`` to their position inside ``x``.
    """
    first_tie = duplicate_method == "first"

    mapping = {}
    for i, val in enumerate(x):
        if not is_missing_scalar(val):
            if not first_tie or val not in mapping:
                mapping[val] = i

    return mapping
