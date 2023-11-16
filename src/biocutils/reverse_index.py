from typing import Sequence


def build_reverse_index(obj: Sequence[str]):
    """Build a reverse index by name, for fast lookup operations.

    Only contains the first occurence of a term.

    Args:
        obj: List of names.

    Returns:
        A map of keys and their index positions.
    """
    revmap = {}
    for i, n in enumerate(obj):
        if n not in revmap:
            revmap[n] = i

    return revmap
