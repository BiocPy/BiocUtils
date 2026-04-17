from typing import Any, Union, Sequence, Optional
from functools import singledispatch

import numpy

from .subset import subset
from .Factor import Factor


@singledispatch
def order(
    x: Any,
    force_last: Union[set, Sequence] = [None, numpy.ma.masked, numpy.nan],
    decreasing: bool = False,
    dtype: Optional[numpy.dtype] = None,
) -> numpy.ndarray:
    """
    Obtain an ordering of entries of ``x``.
    This ordering should be stable.

    Args:
        x:
            Values to be ordered.
            All values should be comparable aside from those listed in ``force_last``.

        force_last:
            Values that are incomparable and will be placed last, i.e., at the end of the ordering.
            No attempt is made to order values within ``force_last``.

        decreasing:
            Whether to order by decreasing value.
            Default is to order by increasing value.

        dtype:
            Integer type of the output array.
            If ``None``, defaults to the smallest type that can hold the length of ``x``.

    Returns:
        Integer NumPy array containing the ordering required to permute ``x`` into a sorted state,
        i.e., given an output array ``o``, ``subset(x, o)`` will be sorted.

    Examples:
        >>> import biocutils
        >>>
        >>> x = [
        ...     15,
        ...     1,
        ...     22,
        ...     3,
        ...     14,
        ... ]
        >>> o = biocutils.order(
        ...     x
        ... )
        >>> print(o)
        >>> biocutils.subset(
        ...     x, o
        ... )
        >>> o = biocutils.order(
        ...     x,
        ...     decreasing=True,
        ... )
        >>> print(o)
        >>> biocutils.subset(
        ...     x, o
        ... )
        >>>
        >>> x = [
        ...     "C",
        ...     "B",
        ...     None,
        ...     "D",
        ...     "D",
        ...     None,
        ...     "A",
        ... ]
        >>> o = biocutils.order(
        ...     x
        ... )
        >>> print(o)
        >>> biocutils.subset(
        ...     x, o
        ... )
        >>> o = biocutils.order(
        ...     x,
        ...     force_last=set(
        ...         [None, "A"]
        ...     ),
        ... )
        >>> print(o)
        >>> biocutils.subset(
        ...     x, o
        ... )
        >>>
        >>> # Factor ordering respects the ordering in the levels.
        >>> x = biocutils.Factor.from_sequence(
        ...     [
        ...         "C",
        ...         "B",
        ...         "D",
        ...         "A",
        ...         "C",
        ...         "A",
        ...         "D",
        ...     ],
        ...     [
        ...         "D",
        ...         "C",
        ...         "B",
        ...         "A",
        ...     ],
        ... )
        >>> o = biocutils.order(
        ...     x
        ... )
        >>> print(o)
        >>> print(
        ...     biocutils.subset(
        ...         x, o
        ...     )
        ... )
    """

    collected = []
    forced = []
    if len(force_last) > 0:
        for i, y in enumerate(x):
            if y not in force_last:
                collected.append(i)
            else:
                forced.append(i)
    else:
        collected = list(range(len(x)))

    def key(i):
        return x[i]

    collected.sort(key=key, reverse=decreasing)

    if dtype is None:
        dtype = numpy.min_scalar_type(len(x) - 1)
    output = numpy.ndarray(len(x), dtype=dtype)
    output[: len(collected)] = collected
    if len(forced) > 0:
        output[len(collected) :] = forced

    return output


@order.register
def _order_Factor(
    x: Factor,
    force_last: Union[set, Sequence] = set([None]),
    decreasing: bool = False,
    dtype: Optional[numpy.dtype] = None,
) -> numpy.ndarray:
    new_force_last = set()
    for i, lev in enumerate(x.get_levels()):
        if lev in force_last:
            new_force_last.add(i)
    if None in force_last:
        new_force_last.add(-1)

    # For consistency with R, we order by codes.
    return order.registry[object](x.get_codes(), force_last=new_force_last, decreasing=decreasing, dtype=dtype)


@singledispatch
def sort(x: Any, force_last: Union[set, Sequence] = [None, numpy.ma.masked], decreasing: bool = False) -> Any:
    """
    Sort an arbitrary iterable sequence.

    Args:
        x:
            Values to be sorted.
            All values should be comparable aside from those listed in ``force_last``.

        force_last:
            Values that are incomparable and will be placed last, i.e., at the end of the ordering.
            No attempt is made to order values within ``force_last``.

        decreasing:
            Whether to sort by decreasing value.
            Default is to sort by increasing value.

    Returns:
        Sorted contents of ``x``.
        This is usually of the same class as ``x``.

    Examples:
        >>> import biocutils
        >>> biocutils.sort(
        ...     range(
        ...         20, 10, -1
        ...     )
        ... )
        >>> biocutils.sort(
        ...     [
        ...         "A",
        ...         "B",
        ...         None,
        ...         "C",
        ...         "D",
        ...     ],
        ...     decreasing=True,
        ... )
        >>> import numpy
        >>> biocutils.sort(
        ...     numpy.random.rand(
        ...         10
        ...     )
        ... )
    """
    return subset(x, order(x, force_last=force_last, decreasing=decreasing))
