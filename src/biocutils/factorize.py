from typing import Optional, Sequence, Tuple

import numpy

from .is_missing_scalar import is_missing_scalar
from .match import match


def factorize(
    x: Sequence,
    levels: Optional[Sequence] = None,
    sort_levels: bool = False,
    dtype: Optional[numpy.dtype] = None,
) -> Tuple[list, numpy.ndarray]:
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

        dtype:
            NumPy type of the array of indices, see
            :py:func:`~biocutils.match.match` for details.

    Returns:
        Tuple where the first element is a list of unique levels and the second
        element in a NumPy array containing integer codes, i.e., indices into
        the first list. Indexing the first list by the second array will
        recover ``x``, with the exception of any None or masked values in ``x``
        that will instead be represented by -1 in the second array.
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

    codes = match(x, levels, dtype=dtype)
    return levels, codes
