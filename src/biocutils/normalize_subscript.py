from typing import Any, Optional, Sequence, Tuple, Union

import numpy


def _raise_int(idx: int, length):
    raise IndexError("subscript (" + str(idx) + ") out of range for vector-like object of length " + str(length))


def _is_scalar_bool(sub):
    return isinstance(sub, bool) or isinstance(sub, numpy.bool_)


class NormalizedSubscript:
    """
    Subscript normalized by :py:func:`~normalize_subscript`. This
    is used to indicate that no further normalization is required,
    such that :py:func:`~normalize_subscript` is just a no-op.
    """

    def __init__(self, subscript: Sequence[int]) -> None:
        """Initialize a NormalizedSubscript.

        Args:
            subscript:
                Sequence of integers for a normalized subscript.
        """
        self._subscript = subscript

    @property
    def subscript(self) -> Sequence[int]:
        """
        Returns:
            The subscript, as a sequence of integer positions.
        """
        return self._subscript

    def __getitem__(self, index: Any) -> Any:
        """Get an item from the subscript.

        Args:
            index: Any argument accepted by the ``__getitem__`` method of the
                subscript.

        Returns:
            The same return value as the ``__getitem__`` method of the
            subscript. This should be an integer if ``index`` is an integer.
        """
        return self._subscript[index]

    def __len__(self) -> int:
        """Get the length of the subscript.

        Returns:
            Length of the subscript.
        """
        return len(self._subscript)


SubscriptTypes = Union[slice, range, Sequence, int, str, bool, NormalizedSubscript]


def normalize_subscript(
    sub: SubscriptTypes,
    length: int,
    names: Optional[Sequence[str]] = None,
    non_negative_only: bool = True,
) -> Tuple[Sequence[int], bool]:
    """Normalize a subscript into a sequence of integer indices.

    Normalize a subscript for ``__getitem__`` or friends into a sequence of
    integer indices, for consistent downstream use.

    Args:
        sub:
            The subscript. This can be any of the following:

            - A slice.
            - A range containing indices to elements. Negative values are
              allowed. An error is raised if the indices are out of range.
            - A single integer specifying the index of an element. A negative
              value is allowed. An error is raised if the index is out of range.
            - A single string that can be found in ``names``, which is
              converted to the index of the first occurrence of that string in
              ``names``. An error is raised if the string cannot be found.
            - A single boolean, which is converted into a list containing the
              first element if true, and an empty list if false.
            - A sequence of strings, integers and/or booleans. Strings are
              converted to indices based on first occurrence in ``names``,
              as described above. Integers should be indices to an element.
              Each truthy boolean is converted to an index equal to its
              position in ``sub``, and each Falsey boolean is ignored.
            - A :py:class:`~NormalizedSubscript`, in which case the
              ``subscript`` property is directly returned.

        length:
            Length of the object.

        names:
            List of names for each entry in the object. If not None, this
            should have length equal to ``length``. Some optimizations
            are possible if this is a :py:class:`~Names.names` object.

        non_negative_only:
            Whether negative indices must be converted into non-negative
            equivalents. Setting this to `False` may improve efficiency.

    Returns:
        A tuple containing (i) a sequence of integer indices in ``[0, length)``
        specifying the subscript elements, and (ii) a boolean indicating whether
        ``sub`` was a scalar.
    """
    if isinstance(sub, NormalizedSubscript):
        return sub.subscript, False

    if _is_scalar_bool(sub):  # before ints, as bools are ints.
        if sub:
            return [0], True
        else:
            return [], False

    if isinstance(sub, int) or isinstance(sub, numpy.integer):
        if sub < -length or sub >= length:
            _raise_int(sub, length)
        if sub < 0 and non_negative_only:
            sub += length
        return [int(sub)], True

    if isinstance(sub, str):
        if names is None:
            raise IndexError("failed to find subscript '" + sub + "' for vector-like object with no names")
        i = -1
        from .names import Names

        if isinstance(names, Names):
            i = names.map(sub)
        else:
            for j, n in enumerate(names):
                if n == sub:
                    i = j
                    break
        if i < 0:
            raise IndexError("cannot find subscript '" + sub + "' in the names")
        return [i], True

    if isinstance(sub, slice):
        return range(*sub.indices(length)), False
    if isinstance(sub, range):
        if len(sub) == 0:
            return [], False

        first = sub[0]
        last = sub[-1]
        if first >= length:
            _raise_int(first, length)
        if last >= length:
            _raise_int(last, length)
        if first < -length:
            _raise_int(first, length)
        if last < -length:
            _raise_int(last, length)

        if not non_negative_only:
            return sub, False
        else:
            if sub.start < 0:
                if sub.stop < 0:
                    return range(length + sub.start, length + sub.stop, sub.step), False
                else:
                    return [(x < 0) * length + x for x in sub], False
            else:
                if sub.stop < 0:
                    return [(x < 0) * length + x for x in sub], False
                else:
                    return sub, False

    can_return_early = True
    for x in sub:
        if isinstance(x, str) or _is_scalar_bool(x) or (x < 0 and non_negative_only):
            can_return_early = False
            break

    if can_return_early:
        for x in sub:
            if x >= length or x < -length:
                _raise_int(x, length)
        return sub, False

    output = []
    has_strings = set()
    string_positions = []
    from .names import Names

    are_names_indexed = isinstance(names, Names)

    for i, x in enumerate(sub):
        if isinstance(x, str):
            if are_names_indexed:
                i = names.map(x)
                if i < 0:
                    raise IndexError("cannot find subscript '" + x + "' in the names")
                output.append(i)
            else:
                has_strings.add(x)
                string_positions.append(len(output))
                output.append(None)
        elif _is_scalar_bool(x):
            if x:
                output.append(i)
        elif x < 0:
            if x < -length:
                _raise_int(x, length)
            output.append(int(x) + length)
        else:
            if x >= length:
                _raise_int(x, length)
            output.append(int(x))

    if len(has_strings):
        if names is None:
            raise IndexError("cannot find string subscripts for vector-like object with no names")

        mapping = {}
        for i, y in enumerate(names):
            if y in has_strings:
                mapping[y] = i
                has_strings.remove(y)  # remove it so we only consider the first.

        for i in string_positions:
            output[i] = mapping[sub[i]]

    return output, False
