from typing import Sequence


def build_reverse_index(obj: Sequence[str]) -> dict:
    """Build a reverse index by name, for fast lookup operations.

    Only contains the first occurrence of a term.

    Args:
        obj: List of names.

    Returns:
        A dictionary mapping names to their index positions.
    """
    revmap = {}
    for i, n in enumerate(obj):
        if n not in revmap:
            revmap[n] = i

    return revmap
