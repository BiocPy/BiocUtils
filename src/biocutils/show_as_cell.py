from typing import Sequence, List, Any, Optional
from functools import singledispatch


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
        output.append(str(x[i]))
    return output
