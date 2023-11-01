from typing import Optional, Sequence, Tuple


def factor(
    x: Sequence, levels: Optional[Sequence] = None, sort_levels: bool = False
) -> Tuple[list, list]:
    """Convert a sequence of hashable values into a factor.

    Args:
        x (Sequence): A sequence of hashable values.
            Any value may be None to indicate missingness.

        levels (Sequence, optional):
            Sequence of reference levels, against which the entries in ``x`` are compared.
            If None, this defaults to all unique values of ``x``.

        sort_levels (bool):
            Whether to sort the automatically-determined levels.
            If False, the levels are kept in order of their appearance in ``x``.
            Not used if ``levels`` is explicitly supplied.

    Returns:
        Tuple[list, list]: Tuple where the first list contains the unique levels
        and the second list contains the integer index into the first list.
        Indexing the first list by the second list will recover ``x``, except
        for any None values in ``x``, which will be None in the second list.
    """

    if levels is None:
        present = set()
        levels = []
        for val in x:
            if val is not None and val not in present:
                levels.append(val)
                present.add(val)
        if sort_levels:
            levels.sort()

    mapping = {}
    for i, lev in enumerate(levels):
        if lev is not None and lev not in mapping:
            mapping[lev] = i

    indices = []
    for i, val in enumerate(x):
        if val is None or val not in mapping:
            indices.append(None)
        else:
            indices.append(mapping[val])

    return levels, indices
