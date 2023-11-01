from typing import Any, Sequence, Union


def subset(x: Any, indices: Union[Sequence[int], slice]) -> Any:
    """Subset ``x`` by ``indices`` to obtain a new object with the desired
    subset of elements. This attempts to use ``x``'s ``__getitem__`` method, if
    available; otherwise it falls back to iteration over the indices.

    If ``x`` has a ``shape`` method that returns a tuple (a la NumPy arrays),
    subsetting is only attempted on the first dimension via the ``__getitem__``
    method. The full extents of all other dimensions are retained.

    Args:
        x:
            Any object that supports ``__getitem__`` with a single index;
            or with a slice and an arbitrary sequence of integer indices.

        indices (Union[Sequence[int], slice):
            Sequence of integers or a slice, specifying the set of elements
            of ``x`` to extract.

    Returns:
        Any: The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns, if it
        accepts a slice and/or sequence of indices. Otherwise, a list is
        returned containing the desired entries of ``x``.
    """
    if not isinstance(x, list):
        try:
            if hasattr(x, "shape") and isinstance(x.shape, tuple) and len(x.shape) > 0:
                expanded = [slice(None)] * len(x.shape)
                expanded[0] = indices
                return x[(*expanded,)]
            else:
                return x[indices]
        except Exception:
            pass

    if isinstance(indices, slice):
        indices = range(*indices.indices(len(x)))
    return [x[i] for i in indices]
