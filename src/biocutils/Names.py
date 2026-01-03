from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

from .assign_sequence import assign_sequence
from .combine_sequences import combine_sequences
from .normalize_subscript import NormalizedSubscript, normalize_subscript
from .reverse_index import build_reverse_index
from .subset_sequence import subset_sequence

SubscriptTypes = Union[slice, range, Sequence, int, bool, NormalizedSubscript]


class Names:
    """
    List of strings containing names. Typically used to decorate sequences,
    such that callers can get or set elements by name instead of position.
    """

    def __init__(self, names: Optional[Iterable] = None, _validate: bool = True):
        """
        Args:
            names:
                Some iterable object containing strings, or values that can
                be coerced into strings.

            _validate:
                Internal use only.
        """
        if _validate:
            if names is None:
                names = []
            elif isinstance(names, Names):
                names = names._names
            else:
                names = list(str(y) for y in names)
        self._names = names
        self._reverse = None

    # Enable fast indexing by name, but only on demand. This reverse mapping
    # field is strictly internal and should be completely transparent to the
    # user; so, calls to map() can be considered as 'non-mutating', as it
    # shouldn't manifest in any visible changes to the Names object. I guess
    # that things become a little hairy in multi-threaded contexts where I
    # should probably protect the final assignment to _reverse. But then
    # again, Python is single-threaded anyway, so maybe it doesn't matter.
    def _populate_reverse_index(self):
        if self._reverse is None:
            self._reverse = build_reverse_index(self._names)

    def _wipe_reverse_index(self):
        self._reverse = None

    ###################################
    #####>>>> Bits and pieces <<<<#####
    ###################################

    def __len__(self) -> int:
        """
        Returns:
            Length of the list.
        """
        return len(self._names)

    def __iter__(self) -> "list_iterator":
        """
        Returns:
            An iterator on the underlying list of names.
        """
        return iter(self._names)

    def __repr__(self) -> str:
        """
        Returns:
            A stringified representation of this object.
        """
        return type(self).__name__ + "(" + repr(self._names) + ")"

    def __str__(self) -> str:
        """
        Returns:
            A pretty-printed representation of this object.
        """
        return str(self._names)

    def __eq__(self, other: Names) -> bool:
        """
        Args:
            other: Another ``Names`` object.

        Returns:
            Whether the current object is the same as ``other``.
        """
        if not isinstance(other, Names):
            return False
        return self._names == other._names

    def as_list(self) -> List[str]:
        """
        Returns:
            List of strings containing the names.

            This should be treated as a read-only reference. Modifications
            should be performed by creating a new ``Names`` object instead.
        """
        return self._names

    def map(self, name: str) -> int:
        """
        Args:
            name: Name of interest.

        Returns:
            Index containing the position of the first occurrence of ``name``;
            or -1, if ``name`` is not present in this object.
        """
        self._populate_reverse_index()
        if name in self._reverse:
            return self._reverse[name]
        else:
            return -1

    def __contains__(self, name: str) -> bool:
        """
        Args:
            name:
                Name to check.

        Returns:
            True if ``name`` exists, otherwise False.
        """
        return self.map(name) >= 0

    #################################
    #####>>>> Get/set items <<<<#####
    #################################

    def get_value(self, index: int) -> str:
        """
        Args:
            index: Position of interest.

        Returns:
            The name at the specified position.
        """
        return self._names[index]

    def get_slice(self, index: SubscriptTypes) -> Names:
        """
        Args:
            index:
                Positions of interest, see the allowed indices in
                :py:func:`~biocutils.normalize_subscript.normalize_subscript`
                for more details. Scalars are treated as length-1 sequences.

        Returns:
            A ``Names`` object containing the names at the specified positions.
        """
        index, scalar = normalize_subscript(index, len(self), None)
        return type(self)(subset_sequence(self._names, index), _validate=False)

    def __getitem__(self, index: SubscriptTypes) -> Union[str, Names]:
        """
        If ``index`` is a scalar, this is an alias for :py:attr:`~get_value`.

        If ``index`` is a sequence, this is an alias for :py:attr:`~get_slice`.
        """
        index, scalar = normalize_subscript(index, len(self), None)
        if scalar:
            return self.get_value(index[0])
        else:
            return self.get_slice(NormalizedSubscript(index))

    def set_value(self, index: int, value: str, in_place: bool = False) -> Names:
        """
        Args:
            index: Position of interest.

            value: Replacement name.

            in_place: Whether to perform the modification in-place.

        Returns:
            A modified ``Names`` object with the replacement name, either as a
            new object or as a reference to the current object.
        """
        if in_place:
            self._wipe_reverse_index()
            output = self
        else:
            output = self.copy()
        output._names[index] = str(value)
        return output

    def set_slice(self, index: SubscriptTypes, value: Sequence[str], in_place: bool = False) -> Names:
        """
        Args:
            index: Positions of interest.

            value: Replacement names.

            in_place: Whether to perform the modification in-place.

        Returns:
            A modified ``Names`` object with the replacement name, either as a
            new object or as a reference to the current object.
        """
        if in_place:
            self._wipe_reverse_index()
            output = self
        else:
            output = self.copy()

        if isinstance(value, Names):
            value = value.as_list()

        index, scalar = normalize_subscript(index, len(self), None)
        output._wipe_reverse_index()
        for i, j in enumerate(index):
            output._names[j] = str(value[i])
        return output

    def __setitem__(self, index: SubscriptTypes, value: Any):
        """
        If ``index`` is a scalar, this is an alias for :py:attr:`~set_value`
        with ``in_place = True``.

        If ``index`` is a sequence, this is an alias for :py:attr:`~set_slice`
        with ``in_place = True``.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            self.set_value(index[0], value, in_place=True)
        else:
            self.set_slice(NormalizedSubscript(index), value, in_place=True)

    ################################
    #####>>>> List methods <<<<#####
    ################################

    def _define_output(self, in_place: bool) -> Names:
        if in_place:
            return self
        else:
            return self.copy()

    def safe_append(self, value: str, in_place: bool = False) -> Names:
        """
        Args:
            value: Name to be added.

            in_place: Whether to perform this appending in-place.

        Returns:
            A ``Names`` object is returned with the added name. This may be a
            new object or a reference to the current object.
        """
        output = self._define_output(in_place)
        name = str(value)
        if output._reverse is not None and name not in output._reverse:
            output._reverse[name] = len(output)
        output._names.append(name)
        return output

    def append(self, value: str):
        """Alias for :py:attr:`~safe_append` with ``in_place = True``."""
        self.safe_append(value, in_place=True)

    def safe_insert(self, index: int, value: str, in_place: bool = False) -> Names:
        """
        Args:
            index: Position on the object to insert at.

            value: Name to be added.

            in_place: Whether to perform this insertion in-place.

        Returns:
            A ``Names`` object is returned with the inserted name. This may be
            a new object or a reference to the current object.
        """
        output = self._define_output(in_place)
        output._wipe_reverse_index()
        output._names.insert(index, str(value))
        return output

    def insert(self, index: int, value: str):
        """Alias for :py:attr:`~safe_insert` with ``in_place = True``."""
        self.safe_insert(index, value, in_place=True)

    def safe_extend(self, value: Sequence[str], in_place: bool = False) -> Names:
        """
        Args:
            value: Names to be added.

            in_place: Whether to perform this extension in-place.

        Returns:
            A ``Names`` object is returned with the extension. This may be a
            new object or a reference to the current object.
        """
        output = self._define_output(in_place)
        if output._reverse is not None:
            for i, n in enumerate(value):
                n = str(n)
                if n not in output._reverse:
                    output._reverse[n] = len(output._names)
                output._names.append(n)
        elif isinstance(value, Names):
            output._names.extend(value._names)
        else:
            output._names.extend(str(y) for y in value)
        return output

    def extend(self, value: Sequence[str]):
        """Alias for :py:attr:`~safe_extend` with ``in_place = True``."""
        self.safe_extend(value, in_place=True)

    def __add__(self, other: list):
        """
        Args:
            other: List of names.

        Returns:
            A new ``Names`` containing the combined contents
            of the current object and ``other``.
        """
        return self.safe_extend(other)

    def __iadd__(self, other: list):
        """
        Args:
            other: List of names.

        Returns:
            The current object is modified by adding ``other`` to its names.
        """
        self.extend(other)
        return self

    def safe_delete(self, index: Union[int, slice], in_place: bool = False) -> Names:
        """
        Args:
            index:
                Position(s) of the name(s) to delete.

            in_place:
                Whether to perform this deletion in-place.

        Returns:
            A ``Names`` object with the deleted name(s). This is a new object
            if ``in_place = False``, otherwise it is a reference to the current
            object.
        """
        output = self._define_output(in_place)
        if in_place:
            output._wipe_reverse_index()

        del output._names[index]
        return output

    def delete(self, index: Union[int, slice]):
        """Alias for :py:attr:`~safe_delete` with ``in_place = True``."""
        self.safe_delete(index, in_place=True)

    def __delitem__(self, index: Union[int, slice]):
        """Alias for :py:attr:`~delete`."""
        self.delete(index)

    ################################
    #####>>>> Copy methods <<<<#####
    ################################

    def copy(self) -> Names:
        """
        Returns:
            A shallow copy of the current object. This will copy the underlying
            list so that any in-place operations like :py:attr:`~append`, etc.,
            on the new object will not change the original object.
        """
        return type(self)(self._names.copy(), _validate=False)

    def __copy__(self) -> Names:
        """Alias for :py:attr:`~copy`."""
        return self.copy()

    def __deepcopy__(self, memo=None, _nil=[]) -> Names:
        """
        Args:
            memo:
                See :py:func:`~copy.deepcopy` for details.

            _nil:
                See :py:func:`~copy.deepcopy` for details.

        Returns:
            A deep copy of this ``Names`` object with the same contents.
        """
        return type(self)(deepcopy(self._names, memo, _nil), _validate=False)

    @property
    def is_unique(self) -> bool:
        """
        Returns:
            True if all names are unique, otherwise False.
        """
        self._populate_reverse_index()
        return len(self._reverse) == len(self._names)


@subset_sequence.register
def _subset_sequence_Names(x: Names, indices: Sequence[int]) -> Names:
    return x.get_slice(NormalizedSubscript(indices))


@assign_sequence.register
def _assign_sequence_Names(x: Names, indices: Sequence[int], other: Sequence) -> Names:
    return x.set_slice(NormalizedSubscript(indices), other)


@combine_sequences.register
def _combine_sequences_Names(*x: Names) -> Names:
    output = x[0].copy()
    for i in range(1, len(x)):
        output.extend(x[i])
    return output


def _name_to_position(names: Optional[Names], index: str) -> int:
    i = -1
    if names is not None:
        i = names.map(index)
    if i < 0:
        raise KeyError("failed to find entry with name '" + index + "'")
    return i


def _validate_names(names: Optional[Names], length: int) -> bool:
    if names is not None and len(names) != length:
        raise ValueError("length of 'names' must be equal to number of entries (" + str(length) + ")")

    return True


def _sanitize_names(names: Optional[Names], length: int) -> Optional[Names]:
    if names is None:
        return names
    if not isinstance(names, Names):
        names = Names(names)

    _validate_names(names, length=length)
    return names


def _combine_names(*x: Any, get_names: Callable) -> Optional[Names]:
    all_names = []
    has_names = False
    for y in x:
        n = get_names(y)
        if n is None:
            all_names.append(len(y))
        else:
            has_names = True
            all_names.append(n)

    if not has_names:
        return None
    else:
        output = Names()
        for i, n in enumerate(all_names):
            if not isinstance(n, Names):
                output.extend([""] * n)
            else:
                output.extend(n)
        return output
