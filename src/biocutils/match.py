from typing import Any, Optional, Literal
from functools import singledispatch

import numpy

from .is_missing_scalar import is_missing_scalar


class MatchIndex:
    """
    An index for matching one or more ``x`` against different ``targets``.
    This is typically constructed by :py:func:`~create_match_index`.
    """

    def __init__(
        self,
        targets: Any,
        duplicate_method: Literal["first", "last", "any"] = "first",
        dtype: Optional[numpy.dtype] = None,
        fail_missing: Optional[bool] = None,
    ):
        """
        Args:
            targets:
                Targets to be matched against, see :py:func:`~match` for details.

            duplicate_method:
                How to handle duplicate entries in ``targets``, see :py:func:`~match` for details.

            dtype:
                NumPy type of the output array, see :py:func:`~match` for details.

            fail_missing:
                Whether to raise an error if a value cannot be found in ``targets``, see :py:func:`~match` for details.
        """

        from .Factor import Factor

        if isinstance(targets, dict):
            # Back-compatible behavior.
            import warnings

            warnings.warn(DeprecationWarning("'map_to_index()' is deprecated, use 'create_match_index()' instead"))
            self._map = targets

        elif isinstance(targets, Factor):
            # Optimized method when both x and targets are factors.
            target_index = [None] * len(targets.get_levels())
            first_tie = duplicate_method == "first" or duplicate_method == "any"
            for i, code in enumerate(targets.get_codes()):
                if code < 0:
                    continue
                if not first_tie or target_index[code] is None:
                    target_index[code] = i

            mapping = {}
            for i, lev in enumerate(targets.get_levels()):
                candidate = target_index[i]
                if candidate is not None:
                    mapping[lev] = candidate
            self._map = mapping

        else:
            first_tie = duplicate_method == "first" or duplicate_method == "any"
            mapping = {}
            for i, val in enumerate(targets):
                if not is_missing_scalar(val):
                    if not first_tie or val not in mapping:
                        mapping[val] = i
            self._map = mapping

        if dtype is None:
            dtype = numpy.min_scalar_type(-len(targets))  # get a signed type
        self._dtype = dtype

        if fail_missing is None:
            fail_missing = numpy.issubdtype(dtype, numpy.unsignedinteger)
        self._fail_missing = fail_missing

    def match(self, x: Any) -> numpy.ndarray:
        """
        Args:
            x:
                Values to match against ``targets``.

        Returns:
            NumPy array of length equal to ``x``, containing the integer position of each entry of ``x`` inside ``targets``;
            see :py:func:`~match` for more details.
        """

        from .Factor import Factor

        indices = numpy.zeros(len(x), dtype=self._dtype)

        if not isinstance(x, Factor):
            # Separate loops to reduce branching in the tight inner loop.
            if not self._fail_missing:
                for i, y in enumerate(x):
                    if y in self._map:
                        indices[i] = self._map[y]
                    else:
                        indices[i] = -1
            else:
                for i, y in enumerate(x):
                    if y not in self._map:
                        raise ValueError("cannot find '" + str(y) + "' in 'targets'")
                    indices[i] = self._map[y]

        else:
            x_index = [-1] * len(x.get_levels())
            for i, lev in enumerate(x.get_levels()):
                if lev in self._map:
                    candidate = self._map[lev]
                    if candidate is not None:
                        x_index[i] = candidate

            # Separate loops to reduce branching in the tight inner loop.
            if self._fail_missing:
                for i, code in enumerate(x.get_codes()):
                    candidate = -1
                    if code >= 0:
                        candidate = x_index[code]
                    if candidate < 0:
                        raise ValueError("cannot find '" + x[i] + "' in 'targets'")
                    indices[i] = candidate
            else:
                for i, code in enumerate(x.get_codes()):
                    if code >= 0:
                        indices[i] = x_index[code]
                    else:
                        indices[i] = -1

        return indices


@singledispatch
def create_match_index(
    targets: Any,
    duplicate_method: Literal["first", "last", "any"] = "first",
    dtype: Optional[numpy.dtype] = None,
    fail_missing: Optional[bool] = None,
) -> MatchIndex:
    """
    Create a index for matching an arbitrary sequence against ``targets``.
    Calling ``create_match_index(targets, ...).match(x)`` is equivalent to ``match(x, targets, ...)``.

    Args:
        targets:
            Targets to be matched against, see :py:func:`~match` for details.

        duplicate_method:
            How to handle duplicate entries in ``targets``, see :py:func:`~match` for details.

        dtype:
            NumPy type of the output array, see :py:func:`~match` for details.

        fail_missing:
            Whether to raise an error if a value cannot be found in ``targets``, see :py:func:`~match` for details.

    Returns:
        A ``MatchIndex``.
        Other implementations of ``create_match_index()`` may return any object that has a ``match()`` method.

    Examples:
        >>> import biocutils
        >>> mobj = biocutils.create_match_index(
        ...     [
        ...         "A",
        ...         "B",
        ...         "C",
        ...         "D",
        ...     ]
        ... )
        >>> mobj.match(
        ...     [
        ...         "A",
        ...         "B",
        ...         "B",
        ...         "C",
        ...         "C",
        ...         "D",
        ...         "E",
        ...     ]
        ... )
        >>>
        >>> ft = biocutils.Factor.from_sequence(
        ...     [
        ...         "a",
        ...         "B",
        ...         "c",
        ...         "D",
        ...         "e",
        ...         "B",
        ...         "D",
        ...     ]
        ... )
        >>> fobj = biocutils.create_match_index(
        ...     ft
        ... )
        >>> fx = biocutils.Factor.from_sequence(
        ...     [
        ...         "A",
        ...         "B",
        ...         "B",
        ...         "C",
        ...         "C",
        ...         "D",
        ...         "E",
        ...     ]
        ... )
        >>> fobj.match(fx)
    """

    return MatchIndex(targets, duplicate_method=duplicate_method, dtype=dtype, fail_missing=fail_missing)


@singledispatch
def match(
    x: Any,
    targets: Any,
    duplicate_method: Literal["first", "last", "any"] = "first",
    dtype: Optional[numpy.dtype] = None,
    fail_missing: Optional[bool] = None,
) -> numpy.ndarray:
    """
    Find a matching value of each element of ``x`` in ``targets``.
    Calling ``match(x, targets, ...)`` should be equivalent to ``create_match_index(targets, ...).match(x)``.

    Args:
        x:
            Values to match against ``targets``.

        targets:
            Targets to be matched against.
            It is not strictly necessary that ``x`` is of the same type as ``targets``,
            but entries of ``x`` should be capable of being equal to entries of ``x``.

        duplicate_method:
            How to handle duplicate entries in ``targets``.
            Either the first, last or any occurrence of each target is reported.

        dtype:
            NumPy type of the output array.
            This should be an integer type; if missing values are expected, the type should be a signed integer.
            If ``None``, a suitable signed type is automatically determined.

        fail_missing:
            Whether to raise an error if ``x`` cannot be found in ``targets``.
            If ``None``, this defaults to ``True`` if ``dtype`` is an unsigned type, otherwise it defaults to ``False``.

    Returns:
        NumPy array of length equal to ``x``, containing the integer position of each entry of ``x`` inside ``targets``;
        or -1, if the entry of ``x`` is ``None`` or cannot be found in ``targets``.

    Examples:
        >>> import biocutils
        >>> biocutils.match(
        ...     [
        ...         "A",
        ...         "B",
        ...         "B",
        ...         "C",
        ...         "D",
        ...         "D",
        ...         "E",
        ...     ],
        ...     [
        ...         "A",
        ...         "B",
        ...         "C",
        ...         "D",
        ...     ],
        ... )
        >>>
        >>> fx = biocutils.Factor.from_sequence(
        ...     [
        ...         "A",
        ...         "B",
        ...         "B",
        ...         "C",
        ...         "C",
        ...         "D",
        ...         "E",
        ...     ]
        ... )
        >>> ft = biocutils.Factor.from_sequence(
        ...     [
        ...         "a",
        ...         "B",
        ...         "c",
        ...         "D",
        ...         "e",
        ...         "B",
        ...         "D",
        ...     ]
        ... )
        >>> biocutils.match(
        ...     fx,
        ...     ft,
        ...     duplicate_method="last",
        ... )
    """

    obj = create_match_index(targets, duplicate_method=duplicate_method, dtype=dtype, fail_missing=fail_missing)
    return obj.match(x)
