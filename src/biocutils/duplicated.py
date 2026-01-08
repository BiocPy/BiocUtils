from typing import Any, Union, Sequence

import numpy

from .Factor import Factor


@singledispatch
def duplicated(x: Any, incomparables: Union[set, Sequence] = set(), from_last: bool = False) -> numpy.ndarray:
    """
    Find duplicated elements of ``x``.

    Args:
        x:
            Object to be searched for duplicates.
            This is usually a sequence that can be iterated over. 

        incomparables:
            Values of ``x`` that cannot be compared.
            Any value of ``x`` in ``incomparables`` will never be a duplicate. 
            Any object that has an ``__in__`` method can be used here.

        from_last:
            Whether to report the last occurrence as a non-duplicate.

    Returns:
        NumPy array of length equal to that of ``x``,
        containing truthy values for only the first occurrence of each value of ``x``.
        If ``from_last = True``, truthy values are only reported for the last occurrence of each value of ``x``.
    """
    available = set()
    output = numpy.ndarray(len(x), dtype=numpy.bool_)

    def process(i, y):
        if y in incomparables:
            output[i] = False
        elif y in available:
            output[i] = True
        else:
            available.add(y)
            output[i] = False

    if not from_last:
        for i, y in enumerate(x):
            process(i, y)
    else:
        for i in range(len(x) - 1, -1, -1):
            process(i, x[i])

    return output


@duplicated.register
def _duplicated_Factor(x: Factor, incomparables: Union[set, Sequence] = set(), from_last: bool = False) -> numpy.ndarray:
    present = []
    for lev in x.get_levels():
        if lev in incomparables:
            present.append(None)
        else:
            present.append(False)
    
    def process(i, y):
        tmp = present[i]
        if tmp is None:
            output[i] = False
        elif tmp:
            output[i] = True
        else:
            present[i] = True
            output[i] = False

    if not from_last:
        for i, y in enumerate(x):
            process(i, y)
    else:
        for i in range(len(x) - 1, -1, -1):
            process(i, x[i])

    return output


def unique(x: Any, incomparables: Union[set, Sequence] = set(), from_last: bool = False) -> Any:
    """
    Get all unique values of ``x``.

    Args:
        x:
            Object in which to find unique entries.
            This is usually a sequence that can be iterated over. 

        incomparables:
            Values of ``x`` that cannot be compared.
            Any value of ``x`` in ``incomparables`` will never be a duplicate. 
            Any object that has an ``__in__`` method can be used here.

        from_last:
            Whether to retain the last occurrence of each value in ``x``. 
            By default, the first occurrence is retained.

    Returns:
        An object containing unique values of ``x``.
        This is usually of the same class as ``x``.
    """
    return subset(x, numpy.where(duplicated(x))[0])
