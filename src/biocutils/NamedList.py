from typing import Sequence
from copy import deepcopy

from .StringList import StringList


class NamedList(list):
    def __init__(self, iterable: Optional[Iterable] = None, names: Optional[StringList] = None):
        """
        Args:
            iterable:
                Some iterable object. Alternatively None, for an empty list.

            names:
                List of names. This should have same length as ``iterable``.
                If None, defaults to an empty list.
        """
        self._data = data
        if names is None:
            names = StringList()
        if not isinstance(names, StringList):
            names = StringList(names)
        self._names = names
        if len(self._data) != len(self._names):
            raise ValueError("length of 'names' should equal the length of 'data'")

    def __repr__(self):
        return "Named(data=" + repr(self._data) + ", names=" + repr(self._names) + ")"

    def get_names(self) -> StringList:
        """
        Returns:
            Names for the list elements.
        """
        return self._names

    @property
    def names(self) -> StringList:
        """Alias for :py:attr:`~get_names`."""
        return self.get_names()

    def set_names(self, names: StringList, in_place: bool = False) -> "NamedList":
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
        if isinstance(names, StringList):
            names = StringList(names)
        if in_place:
            if len(names) != len(self._data):
                raise ValueError("length of 'names' should equal the length of 'data'")
            self._names = names
            return self
        else:
            return NamedSequence(self, names)

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
            i = self._names.index(index)
            if i < 0:
                raise KeyError("failed to find value with name '" + args + "'")
            return super().__getitem__(i)

        output = super().__getitem__(index)
        if isinstance(index, slice):
            return NamedSequence(output, self._names[index])
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
            i = self._names.index(index)
            if i >= 0:
                return super().__setitem__(i, item)
            else:
                self._names.append(index)
                super().__append__(item)
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
            index = self._names.index(index)
            if index < 0:
                raise KeyError("failed to find value with name '" + args + "'")
        super().insert(index, item)

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
        else:
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
        output._names = self._names.copy()
        output.extend(other)
        return output

    def __iadd__(self, other: list):
        """
        Extend an existing ``NamedList`` with a new list.

        Args:
            other:
                A list of items that can be coerced to strings or are None.

        Returns:
            The current object is extended with the contents of ``other``.
        """
        self.extend(other)
        return self

    def copy(self) -> "NamedList":
        """
        Returns:
            A shallow copy of a ``NamedList`` with the same contents.
        """
        return NamedList(self, names=self._names)

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
