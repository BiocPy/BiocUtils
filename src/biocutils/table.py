from functools import singledispatch
from typing import Sequence

from .integer_list import IntegerList


@singledispatch
def table(x: Sequence, sort: bool = True) -> IntegerList:
    """Create a frequency table of values in a sequence.

    Count the occurrences of each unique value in the input sequence and return
    them as an IntegerList with names corresponding to the unique values.

    Args:
        x:
            A sequence of hashable values.

        sort:
            Whether to sort the output by keys (values from x).

    Returns:
        An IntegerList where names are the unique values and values are their counts.
    """
    output = {}
    for v in x:
        if v in output:
            output[v] += 1
        else:
            output[v] = 1

    if sort:
        collected = sorted(output.keys())
        tmp = {}
        for y in collected:
            tmp[y] = output[y]
        output = tmp

    return IntegerList.from_dict(output)
