from typing import Any, Sequence, Union

from .NamedList import NamedList
from .Factor import Factor
from .match import match
from .subset import subset
from .get_height import get_height


def split(x: Any, f: Sequence, drop: bool = False, as_NamedList: bool = False) -> Union[dict, NamedList]:
    """
    Split a sequence ``x`` into groups defined by a categorical factor ``f``.

    Args:
        x:
            Values to be divided into groups.
            Any object that supports :py:func:`~biocutils.subset.subset` can be used here.

        f:
            A sequence of categorical variables defining the groupings.
            This should have length equal to the "height" of ``x`` (see :py:func:`~biocutils.get_height.get_height`).

            The order of groups is defined by sorting all unique variables in ``f``.
            If a :py:class:`~biocutils.Factor.Factor` is provided, the order of groups is defined by the existing levels.

        drop:
            Whether to drop unused levels, if ``f`` is a ``Factor``.
        
        as_NamedList:
            Whether to return the results as a :py:class:`~biocutils.NamedList.NamedList`.
            This automatically converts all groups into strings.

    Returns:
        A dictionary where each key is a unique group and each value contains that group's entries from ``x``.
        If ``as_NamedList = true``, this is a ``NamedList`` instead.

    Examples:
        >>> import numpy
        >>> x = numpy.random.rand(10)
        >>> f = numpy.random.choice(["A", "B", "C"], 10)
        >>> import biocutils
        >>> biocutils.split(x, f)
        >>> biocutils.split(x, f, as_NamedList=True)
        >>> biocutils.split(x, biocutils.Factor.from_sequence(f, ["X", "A", "Y", "B", "Z", "C"]), drop=False)
    """

    if isinstance(f, Factor):
        if drop:
            f = f.drop_unused_levels()
        levels = f.get_levels()
        indices = f.get_codes()
    else:
        levels = sorted(list(set(f)))
        indices = match(f, levels)

    if get_height(x) != get_height(f):
        raise ValueError("heights of 'x' and 'f' should be the same") 

    collected = []
    for l in levels:
        collected.append([])
    for i, j in enumerate(indices):
        collected[j].append(i)
    for i, c in enumerate(collected):
        collected[i] = subset(x, c)

    if as_NamedList:
        return NamedList(collected, levels)
    else:
        return dict(zip(levels, collected))
