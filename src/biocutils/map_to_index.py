from typing import Sequence, Literal


DUPLICATE_METHOD = Literal["first", "last"]

def map_to_index(x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> dict:
    """Create a dictionary to map the values of a sequence to its positional indices.

    Args:
        x (Sequence): Sequence of hashable values.

        duplicate_method (DUPLICATE_METHOD): Whether to consider the first or
            last occurrence of a duplicated value in ``x``.

    Returns:
        dict: Dictionary that maps values of ``x`` to their position inside ``x``.
    """
    first_tie = duplicate_method == "first"

    mapping = {}
    for i, val in enumerate(x):
        if val is not None:
            if not first_tie or val not in mapping:
                mapping[val] = i

    return mapping
