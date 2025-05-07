from functools import singledispatch
from typing import Any, List, Sequence


@singledispatch
def show_as_cell(x: Any, indices: Sequence[int]) -> List[str]:
    """
    Show the contents of ``x`` as a cell of a table, typically for use in the
    ``__str__`` method of a class that contains ``x``.

    Args:
        x:
            Any object. By default, we assume that it can be treated as
            a sequence, with a valid ``__getitem__`` method for an index.

        indices:
            List of indices to be extracted.

    Returns:
        List of strings of length equal to ``indices``, containing a
        string summary of each of the specified elements of ``x``.
    """
    output = []
    for i in indices:
        try:
            candidate = str(x[i])
            if len(candidate) > 25:
                candidate = candidate[:20] + "..." # pick the first two characters, whatever.
            nl = candidate.find("\n")
            if nl >= 0:
                candidate = candidate[:nl] + "..."
            output.append(candidate)
        except:
            output.append("####")
    return output
