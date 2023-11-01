from typing import Sequence

from .map_to_index import DUPLICATE_METHOD


def intersect(*x: Sequence, duplicate_method: DUPLICATE_METHOD = "first") -> list:
    """Identify the intersection of values in multiple sequences, while preserving the order of values in the first
    sequence.

    Args:
        x (Sequence):
            Zero, one or more sequences of interest.

        duplicate_method (DUPLICATE_METHOD):
            Whether to keep the first or last occurrence of duplicated values
            when preserving order in the first sequence.

    Returns:
        list: Intersection of values across all ``x``. None values are ignored.
    """
    nargs = len(x)
    if nargs == 0:
        return []

    first = x[0]
    if nargs == 1:
        # Special handling of n == 1, for efficiency.
        present = set()
        output = []

        def handler(f):
            if f is not None and f not in present:
                output.append(f)
                present.add(f)

        if duplicate_method == "first":
            for f in first:
                handler(f)
        else:
            for f in reversed(first):
                handler(f)
            output.reverse()

        return output

    # The 'occurrences' dict contains the count and the index of the last
    # sequence that incremented the count. The intersection consists of all
    # values where the count == number of sequences. We need to store the index
    # of the last sequence so as to avoid adding a duplicate value twice from a
    # single sequence.
    occurrences = {}
    for f in first:
        if f is not None and f not in occurrences:
            occurrences[f] = [1, 0]

    for i in range(1, nargs):
        for f in x[i]:
            if f is not None and f in occurrences:
                state = occurrences[f]
                if state[1] < i:
                    state[0] += 1
                    state[1] = i

    # Going through the first vector again to preserve order.
    output = []

    def handler(f):
        if f is not None and f in occurrences:
            state = occurrences[f]
            if state[0] == nargs and state[1] >= 0:
                output.append(f)
                state[1] = -1  # avoid duplicates

    if duplicate_method == "first":
        for f in first:
            handler(f)
    else:
        for f in reversed(first):
            handler(f)
        output.reverse()

    return output
