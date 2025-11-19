from typing import Any

import numpy


def is_missing_scalar(x: Any) -> bool:
    """Check if a scalar value is missing.

    Args:
        x: Any scalar value.

    Returns:
        Whether ``x`` is None or a NumPy masked constant.
    """
    return x is None or numpy.ma.is_masked(x)
