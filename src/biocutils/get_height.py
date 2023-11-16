from functools import singledispatch
from typing import Any

from .is_high_dimensional import is_high_dimensional


@singledispatch
def get_height(x: Any) -> int:
    """
    Get the "height" of an object, i.e., as if it were a column of a data frame
    or a similar container. This defaults to ``len`` for vector-like objects,
    or the first dimension for high-dimensional objects with a ``shape``.

    Args:
        x:
            Some kind of object.

    Returns:
        The height of the object.
    """
    if is_high_dimensional(x):
        return x.shape[0]
    else:
        return len(x)
