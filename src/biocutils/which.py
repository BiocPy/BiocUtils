from typing import Optional, Sequence
import numpy


def which(
    x: Sequence,
    dtype: Optional[numpy.ndarray] = None,
) -> numpy.ndarray:
    """Report the indices of all elements of ``x`` that are truthy.

    Args:
        x:
            Sequence of values to be interpreted as booleans.

        dtype:
            NumPy type of the output array. This should be an integer type. If
            None, a suitable signed type is automatically determined.

    Returns:
        Array of length no greater than ``x``, containing the indices of all
        truthy entries. Indices are guaranteed to be unique and sorted.
    """
    if isinstance(x, numpy.ndarray):
        found = numpy.where(x)[0]
        if not dtype is None:
            found = found.astype(dtype=dtype, copy=False, order="A")
        return found

    dtype = numpy.min_scalar_type(len(x))
    found = []
    for i, y in enumerate(x):
        if y:
            found.append(i)
    return numpy.array(found, dtype=dtype)
