from functools import singledispatch
from typing import Any


@singledispatch
def is_high_dimensional(x: Any) -> bool:
    """Check if an object is high-dimensional.

    Whether an object is high-dimensional, i.e., has a ``shape``
    attribute that is of length greater than 1.

    Args:
        x:
            Some kind of object.

    Returns:
        Whether ``x`` is high-dimensional.
    """
    return hasattr(x, "shape") and len(x.shape) > 1
