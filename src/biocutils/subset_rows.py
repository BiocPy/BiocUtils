from functools import singledispatch
from typing import Any, Sequence


@singledispatch
def subset_rows(x: Any, indices: Sequence[int]) -> Any:
    """
    Subset ``x`` by ``indices`` on the first dimension. The default
    method attempts to use ``x``'s ``__getitem__`` method,

    Args:
        x:
            Any high-dimensional object.

        indices:
            Sequence of non-negative integers specifying the integers of interest.

    Returns:
        The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns.
    """
    tmp = [slice(None)] * len(x.shape)
    tmp[0] = indices
    return x[(*tmp,)]
