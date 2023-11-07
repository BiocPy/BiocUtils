from typing import Optional, Sequence, Tuple
import numpy

from .match import match
from .is_missing_scalar import is_missing_scalar


def factorize(x: Sequence, levels: Optional[Sequence] = None, sort_levels: bool = False) -> Tuple[list, numpy.ndarray]:
    """Convert a sequence of hashable values into a factor.

    Args:
        x: 
            A sequence of hashable values.
            Any value may be None to indicate missingness.

        levels:
            Sequence of reference levels, against which the entries in ``x`` are compared.
            If None, this defaults to all unique values of ``x``.

        sort_levels:
            Whether to sort the automatically-determined levels.
            If False, the levels are kept in order of their appearance in ``x``.
            Not used if ``levels`` is explicitly supplied.

    Returns:
        Tuple where the first list contains the unique levels and the second
        array contains the integer index into the first list. Indexing the
        first list by the second array will recover ``x``; except for any None
        or masked values in ``x``, which will be -1 in the second array.
    """

    if levels is None:
        present = set()
        levels = []
        for val in x:
            if not is_missing_scalar(val) and val not in present:
                levels.append(val)
                present.add(val)
        if sort_levels:
            levels.sort()

    codes = match(x, levels)
    return levels, codes
