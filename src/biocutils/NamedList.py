from typing import Sequence, Optional, Iterable, Union, Any
from copy import deepcopy

from .Names import Names
from .subset_sequence import subset_sequence
from .combine_sequences import combine_sequences
from .assign_sequence import assign_sequence


class NamedList(list):
    """
    A Python list with a name for each element, equivalent to R's named list.
    This provides some dict-like behavior, with methods to index by name in
    addition to the usual indexing by integer positions or slices.
    """

    def __init__(self, iterable: Optional[Iterable] = None, names: Optional[Names] = None):
        """
        Args:
            iterable:
                Some iterable object. Alternatively None, for an empty list.

            names:
                List of names. This should have same length as ``iterable``.
                If None, defaults to an empty list.
        """
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)

        if names is None:
            if isinstance(iterable, NamedList):
                names = iterable._names
            else:
                names = Names()
        elif not isinstance(names, Names):
            names = Names(names)
        self._names = names
        if len(self) != len(self._names):
            raise ValueError("length of 'names' should equal the length of 'data'")

    def __repr__(self):
        return "NamedList(data=" + super().__repr__() + ", names=" + repr(self._names) + ")"

    def __str__(self):
        return "[" + ", ".join(repr(self._names[i]) + "=" + repr(x) for i, x in enumerate(self)) + "]" 

    def get_names(self) -> Names:
        """
        Returns:
            Names for the list elements.
        """
        return self._names

    @property
    def names(self) -> Names:
        """Alias for :py:attr:`~get_names`."""
        return self.get_names()

    def set_names(self, names: Names, in_place: bool = False) -> "NamedList":
        """
        Args:
            names:
                List of names, of the same length as this list.

            in_place:
                Whether to perform this modification in-place.

        Returns:
            A modified ``NamedList`` with the new names. If ``in_place =
            False``, this is a new ``NamedList``, otherwise it is a reference
            to the current ``NamedList``.
        """
        if isinstance(names, Names):
            names = Names(names)
        if in_place:
            if len(names) != len(self._data):
                raise ValueError("length of 'names' should equal the length of 'data'")
            self._names = names
            return self
        else:
            return NamedList(self, names)

    def __getitem__(self, index: Union[str, int, slice]):
        """
        Args:
            index:
                An integer index containing a position to extract, a string
                specifying the name of the value to extract, or a slice
                specifying multiple positions to extract.

        Returns:
            If ``index`` is an integer, the value at the specified position.

            If ``index`` is a string, the value with the specified name. If
            multiple values have the same name, the first is returned.

            If ``index`` is a slice, a new ``NamedList`` is returned
            containing the items at the specified positions.
        """
        if isinstance(index, str):
            i = self._names.map(index)
            if i < 0:
                raise KeyError("no list element named '" + index + "'")
            return super().__getitem__(i)

        output = super().__getitem__(index)
        if isinstance(index, slice):
            return NamedList(output, self._names[index])
        return output


    def __setitem__(self, index: Union[int, str, slice], item: Any):
        """
        Args:
            index:
                An integer index containing a position to set, a string
                specifying the name of the value to set, or a slice specifying
                multiple positions to set.

            item:
                If ``index`` is an integer or string, a value to be set at the
                corresponding position of this ``NamedList``.

                If ``index`` is a slice, an iterable of the same length
                containing values to be set at the sliced positions. If
                ``item`` is a ``NamedList``, the names are also transferred.

        Returns:
            In the current object, the specified item(s) at ``index`` are
            replaced with the contents of ``item``.

            If ``index`` is a string that does not exist in the names, it is
            appended to the names and ``item`` is appended to the list.
        """
        if isinstance(index, slice):
            super().__setitem__(index, item)
            if isinstance(item, type(self)):
                self._names[index] = item._names
        elif isinstance(index, str):
            i = self._names.map(index)
            if i >= 0:
                return super().__setitem__(i, item)
            else:
                super().append(item)
                self._names.append(index)
        else:
            super().__setitem__(index, item)

    def insert(self, index: Union[int, str], item: Any):
        """
        Args:
            index:
                An integer index containing a position to insert at.
                Alternatively, the name of the value to insert at (the first
                occurrence of each name is used).

            item:
                A scalar that can be coerced into a string, or None.

        Returns:
            ``item`` is inserted at ``index`` in the current object.
        """
        if isinstance(index, str):
            i = self._names.map(index)
            if i < 0:
                raise KeyError("no list element named '" + index + "'")
            index = i
        super().insert(index, item)
        self._names.insert(index, "")

    def append(self, item: Any):
        """
        Args:
            item:
                Any value.

        Returns:
            ``item`` is added to the end of the current object, with its name
            set to an empty string.
        """
        self._names.append("")
        super().append(item)

    def extend(self, iterable: Iterable):
        """
        Args:
            iterable: 
                Some iterable object. If this is a ``NamedList``, its names are
                used to extend the names of the current object; otherwise the
                extended names are set to empty strings.

        Returns:
            Items in ``iterable`` are added to the end of the current object.
        """
        super().extend(iterable)
        if isinstance(iterable, NamedList):
            self._names.extend(iterable._names)
        elif len(iterable):
            self._names.extend([""] * len(iterable))

    def __add__(self, other: list) -> "NamedList":
        """
        Args:
            other:
                A list of items to be added to the right of the current object.

        Returns:
            A new ``NamedList`` containing the concatenation of the
            current object's items and those of ``other``.
        """
        output = self.copy()
        output.extend(other)
        return output

    def __iadd__(self, other: list):
        """
        Extend an existing ``NamedList`` with a new list.

        Args:
            other:
                A list of items.

        Returns:
            The current object is extended with the contents of ``other``.  If
            ``other`` is a ``NamedList``, its names are used for extension;
            otherwise the extension is performed with empty strings.
        """
        self.extend(other)
        return self

    def copy(self) -> "NamedList":
        """
        Returns:
            A shallow copy of a ``NamedList`` with the same contents.
        """
        return NamedList(self, names=self._names.copy())

    def __deepcopy__(self, memo=None, _nil=[]) -> "NamedList":
        """
        Args:
            memo:
                See :py:func:`~copy.deepcopy` for details.

            _nil:
                See :py:func:`~copy.deepcopy` for details.

        Returns:
            A deep copy of a ``NamedList`` with the same contents.
        """
        return NamedList(deepcopy(self, memo, _nil), names=deepcopy(self_names, memo, _nil))


@subset_sequence.register
def _subset_sequence_NamedList(x: NamedList, indices: Sequence[int]) -> NamedList:
    return NamedList((x[i] for i in indices), names=subset_sequence(x._names, indices))


@combine_sequences.register
def _combine_sequences_NamedList(*x: NamedList) -> NamedList:
    output = x[0].copy()
    for i in range(1, len(x)):
        output.extend(x[i])
    return output


@assign_sequence.register
def _assign_sequence_NamedList(x: NamedList, indices: Sequence[int], other) -> NamedList:
    output = assign_sequence.registry[list](x, indices, other)
    if isinstance(other, NamedList):
        output._names = assign_sequence(output._names, indices, other._names)
    return output
