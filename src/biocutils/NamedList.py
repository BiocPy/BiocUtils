from typing import Sequence, Optional, Iterable, Union, Any, Dict
from copy import deepcopy

from .Names import Names
from .subset_sequence import subset_sequence
from .combine_sequences import combine_sequences
from .assign_sequence import assign_sequence


def _name_to_position(names: Optional[Names], index: str) -> int:
    i = -1
    if names is not None:
        i = names.map(index)
    if i < 0:
        raise KeyError("failed to find entry with name '" + index + "'")
    return i


def _sanitize_names(names: Optional[Names], length: int) -> Union[None, Names]:
    if names is None:
        return names
    if isinstance(names, Names):
        names = Names(names)
    if len(names) != length:
        raise ValueError("length of 'names' must be equal to number of entries (" + str(length) + ")")
    return names


class NamedList:
    """
    A list-like object that may have names for each element, equivalent to R's
    named list. This combines list and dictionary functionality, e.g., it can
    be indexed by position or slices (list) but also by name (dictionary).
    """

    def __init__(self, data: Optional[Iterable] = None, names: Optional[Names] = None):
        """
        Args:
            data:
                Sequence of data values.

                Alternatively None, for an empty list.

            names:
                List of names. This should have same length as ``data``.
                Alternatively None, if the list has no valid names yet.
        """
        if data is None:
            self._data = []
        if not isinstance(data, list):
            data = list(data)
        self._data = data
        self._names = _sanitize_names(len(self._data), names)

    def __repr__(self):
        return "NamedList(data=" + repr(self._data) + ", names=" + repr(self._names) + ")"

    def __str__(self):
        return "[" + ", ".join(repr(self._names[i]) + "=" + repr(x) for i, x in enumerate(self._data)) + "]" 

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

    def set_names(self, names: Optional[Names], in_place: bool = False) -> "NamedList":
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
        if in_place:
            output = self
        else:
            output = self.copy()
        output._names = _sanitize_names(len(self), names) 
        return output

    def get_slice(self, sub: Union[str, int, bool, Sequence], normalize: bool = True) -> "NamedList":
        if normalize:
            sub, scalar = normalize_subscript(sub, len(self), self._names)
        outdata = subset_sequence(self._data, sub)
        outnames = None
        if self._names is not None:
            outnames = subset_sequence(self._names, sub)
        return type(self)(outdata, outnames)

    def __getitem__(self, index: Union[str, int, bool, Sequence]):
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
        sub, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            return self._data[sub[0]]
        else:
            return self.get_slice(sub, normalize=False)

    def set_slice(self, index: Union[int, str, slice], value: Sequence, in_place: bool = False, normalize: bool = True):
        if normalize:
            index, scalar = normalize_subscript(index, len(self), self._names)
        if in_place:
            output = self
        else:
            output = self.copy()
            output._data = output._data.copy()
        for i, j in enumerate(index):
            output._data[j] = value[i]
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
        index, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            self._data[index[0]] = item
        else:
            self._slice(index, item, in_place=True, normalize=False)

    def _define_output(self, in_place: bool) -> "NamedList":
        if in_place:
            return self
        newdata = self._data.copy()
        newnames = None
        if self._names is not None:
            newnames = self._names.copy()
        return NamedList(newdata, names=newnames)

    def safe_insert(self, index: Union[int, str], item: Any, in_place: bool = False) -> "NamedList":
        output = self._define_output(in_place)
        if isinstance(index, str):
            index = _name_to_position(self._names, index)
        output._data.insert(index, item)
        if output._names is not None:
            output._names.insert(index, "")
        return output

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
        self.safe_insert(index, item, in_place=True)

    def safe_append(self, item: Any, in_place: bool = False) -> "NamedList":
        output = self._define_output(in_place)
        output._data.append(item)
        if output._names is not None:
            output._names.append("")
        return output

    def append(self, item: Any):
        """
        Args:
            item:
                Any value.

        Returns:
            ``item`` is added to the end of the current object, with its name
            set to an empty string.
        """
        self.safe_append(item, in_place=True)

    def safe_extend(self, other: Iterable, in_place: bool = True):
        """
        Args:
            iterable: 
                Some iterable object. If this is a ``NamedList``, its names are
                used to extend the names of the current object; otherwise the
                extended names are set to empty strings.

        Returns:
            Items in ``iterable`` are added to the end of the current object.
        """
        output = self._define_output(in_place)
        previous_len = len(output)
        output._data.extend(other)

        if isinstance(other, NamedList):
            if output._names is None:
                output._names = Names([""] * previous_len)
            output._names.extend(other._names)
        elif output._names is not None:
            output._names.extend([""] * len(other))

        return output

    def extend(self, other: Iterable):
        self.safe_extend(other, in_place=True)

    def __add__(self, other: list) -> "NamedList":
        """
        Args:
            other:
                A list of items to be added to the right of the current object.

        Returns:
            A new ``NamedList`` containing the concatenation of the
            current object's items and those of ``other``.
        """
        return output.safe_extend(other)

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
        return NamedList(self._data, names=self._names)

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
        return NamedList(deepcopy(self._data, memo, _nil), names=deepcopy(self._names, memo, _nil))

    def as_dict(self) -> dict[str, Any]:
        """
        Returns:
            A dictionary where the keys are the names and the values are the
            list elements. Only the first occurrence of each name is returned.
        """
        output = {}
        for i, n in enumerate(self._names):
            if n not in output:
                output[n] = self[i]
        return output

    @staticmethod
    def from_dict(x: dict) -> "NamedList":
        return NamedList(list(x.values()), names=Names(str(y) for y in x.keys()))


@subset_sequence.register
def _subset_sequence_NamedList(x: NamedList, indices: Sequence[int]) -> NamedList:
    return x.get_slice(indices, normalize=False)


@combine_sequences.register
def _combine_sequences_NamedList(*x: NamedList) -> NamedList:
    output = x[0]._define_output(in_place=False)
    for i in range(1, len(x)):
        output.extend(x[i])
    return output


@assign_sequence.register
def _assign_sequence_NamedList(x: NamedList, indices: Sequence[int], other: Sequence) -> NamedList:
    if isinstance(other, NamedList):
        other = other._data
    return NamedList(assign_sequence(x._data, indices, other), names=x._names)
