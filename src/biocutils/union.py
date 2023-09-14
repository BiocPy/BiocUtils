from typing import Sequence, Tuple

from .map_to_index import DUPLICATE_METHOD


def union(*x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> list:
    """Identify the union of values in multiple sequences, while preserving the
    order of the first (or last) occurence of each value.

    Args:
        x (Sequence): 
            Zero, one or more sequences of interest.

        duplicate_method (DUPLICATE_METHOD): 
            Whether to take the first or last occurrence of each value in the
            ordering of the output. If first, the first occurrence in the
            earliest sequence of ``x`` is reported; if last, the last
            occurrence in the latest sequence of ``x`` is reported.

    Returns:
        list: Union of values across all ``x``. None values are ignored.
    """

    nargs = len(x)
    if nargs == 0:
        return []

    output = []
    present = set()
    def handler(f):
        if f is not None and f not in present:
            output.append(f)
            present.add(f)

    if duplicate_method == "first":
        for a in x:
            for f in a:
                handler(f)
    else:
        for a in reversed(x):
            for f in reversed(a):
                handler(f)
        output.reverse()

    return output
