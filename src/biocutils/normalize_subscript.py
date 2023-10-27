from typing import Union, Sequence, Optional, Tuple


def _raise_int(idx: int, length):
    raise IndexError("subscript (" + str(idx) + ") out of range for vector-like object of length " + str(length))


has_numpy = False
try:
    import numpy
    has_numpy = True
except:
    pass


def normalize_subscript(sub: Union[slice, range, Sequence, int, str, bool], length: int, names: Optional[Sequence[str]] = None) -> Tuple:
    """
    Normalize a subscript for ``__getitem__`` or friends into a sequence of
    integer indices, for consistent downstream use.

    Args:
        sub: 
            The subscript. This can be any of the following:

            - A slice of elements. 
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

        length:
            Length of the object.

        names:
            List of names for each entry in the object. If not None, this
            should have length equal to ``length``.

    Returns:
        A tuple containing (i) a sequence of integer indices in ``[0, length)``
        specifying the subscript elements, and (ii) a boolean indicating whether
        ``sub`` was a scalar.
    """
    if isinstance(sub, bool) or (has_numpy and isinstance(sub, numpy.bool_)): # before ints, as bools are ints.
        if sub:
            return [0], True
        else:
            return [], False

    if isinstance(sub, int) or (has_numpy and isinstance(sub, numpy.generic)):
        if sub < -length or sub >= length:
            _raise_int(sub, length)
        if sub < 0:
            sub += length
        return [int(sub)], True

    if isinstance(sub, str):
        if names is None:
            raise IndexError("failed to find subscript '" + sub + "' for vector-like object with no names")
        return [names.index(sub)], True

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

        if sub.start < 0:
            if sub.stop < 0:
                return range(length + sub.start, length + sub.stop, sub.step), False
            else:
                return [ (x < 0) * length + x for x in sub], False
        else:
            if sub.stop < 0:
                return [ (x < 0) * length + x for x in sub], False
            else:
                return sub, False

    can_return_early = False
    for x in sub:
        if isinstance(x, str) or isinstance(x, bool) or (has_numpy and isinstance(x, numpy.bool_)) or x < 0:
            can_return_early = False;
            break

    if can_return_early:
        for x in sub:
            if x >= length:
                _raise_int(x, length)
        return sub, False

    output = []
    has_strings = set()
    string_positions = []
    for i, x in enumerate(sub):
        if isinstance(x, str):
            has_strings.add(x)
            string_positions.append(len(output))
            output.append(None)
        elif isinstance(x, bool) or (has_numpy and isinstance(x, numpy.bool_)):
            if x:
                output.append(i)
        elif x < 0:
            if x < -length:
                _raise_int(x, length)
            output.append(x + length)
        else:
            if x >= length:
                _raise_int(x, length)
            output.append(x)

    if len(has_strings):
        if names is None:
            raise IndexError("cannot find string subscripts for vector-like object with no names")

        mapping = {}
        for i, y in enumerate(names):
            if y in has_strings:
                mapping[y] = i
                has_strings.remove(y) # remove it so we only consider the first.

        for i in string_positions:
            output[i] = mapping[sub[i]]

    return output, False
