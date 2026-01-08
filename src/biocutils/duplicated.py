from typing import Any, Union, Sequence
from functools import singledispatch

import numpy

from .Factor import Factor
from .subset import subset


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

    Examples:
        >>> import biocutils
        >>> biocutils.duplicated([1,2,1,2,3,2])
        >>> biocutils.duplicated([1,2,1,2,3,2], from_last=True)
        >>> biocutils.duplicated([1,2,None,None,3,2])
        >>> biocutils.duplicated([1,2,None,None,3,2], incomparables=set([None]))
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

    # Handling codes of -1, i.e., None.
    if None in incomparables:
        present.append(None)
    else:
        present.append(False)

    output = numpy.ndarray(len(x), dtype=numpy.bool_)
    def process(i, y):
        tmp = present[y]
        if tmp is None:
            output[i] = False
        elif tmp:
            output[i] = True
        else:
            present[y] = True
            output[i] = False

    if not from_last:
        for i, y in enumerate(x.get_codes()):
            process(i, y)
    else:
        codes = x.get_codes()
        for i in range(len(x) - 1, -1, -1):
            process(i, codes[i])

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

    Examples:
        >>> import biocutils
        >>> biocutils.unique([1,2,1,2,3,2])
        >>> biocutils.unique([1,2,None,None,3,2])
        >>> biocutils.unique([1,2,None,None,3,2], incomparables=set([None]))
    """
    return subset(x, numpy.where(numpy.logical_not(duplicated(x, incomparables=incomparables, from_last=from_last)))[0])
