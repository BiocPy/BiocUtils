import numpy


def is_missing_scalar(x) -> bool:
    """
    Args:
        x:
            Any scalar value.

    Returns:
        Whether ``x`` is None or a NumPy masked constant.
    """
    return x is None or numpy.ma.is_masked(x)
