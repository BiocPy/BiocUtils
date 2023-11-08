from typing import Any, Union, Optional
from collections.abc import Iterable


def _coerce_to_str(x: Any) -> bool:
    return None if x is None else str(x)


class StringList(list):
    """
    Python list of strings. This is the same as a regular Python list except
    that anything added to it will be coerced into a string. None values are
    also acceptable and are treated as missing strings.
    """

    def __init__(self, iterable: Optional[Iterable] = None, coerce: bool = True):
        """
        Args:
            iterable: 
                Some iterable object where all values can be coerced to strings
                or are None. 

                Alternatively this may itself be None, which defaults to an empty list.

            coerce:
                Whether to perform the coercion to strings. This can be skipped
                if it is known that ``iterable`` only contains strings or None.
        """
        if iterable is not None:
            new_it = iterable
            if coerce and not isinstance(iterable, type(self)):
                new_it = (_coerce_to_str(item) for item in iterable)
            super().__init__(new_it)
        else:
            super().__init__()

    def __getitem__(self, index: Union[int, slice]) -> Union[str, "StringList"]:
        """
        Obtain one or more elements from a ``StringList``.

        Args:
            index:
                An integer index containing a position to extract, or a slice
                specifying multiple positions to extract.
            
        Returns:
            If ``index`` is an integer, a string or None is returned at the
            specified position.

            If ``index`` is a slice, a new ``StringList`` is returned
            containing the items at the specified positions.
        """
        output = super().__getitem__(index)
        if isinstance(index, slice):
            return StringList(output, coerce=False)
        return output

    def __setitem__(self, index: Union[int, slice], item: Any):
        """
        Set one or more items in the ``StringList``.

        Args:
            index:
                An integer index containing a position to set, or a slice
                specifying multiple positions to set.

            item:
                If ``index`` is an integer, a scalar that can be coerced into a
                string, or None.

                If ``index`` is a slice, an iterable of the same length
                containing values that can be coerced to strings or None.

        Returns:
            In the current object, the specified item(s) at ``index`` are
            replaced with the contents of ``item``.
        """
        if isinstance(index, slice):
            new_it = item
            if not isinstance(item, type(self)):
                new_it = (_coerce_to_str(x) for x in item)
            super().__setitem__(index, new_it)
        else:
            super().__setitem__(index, _coerce_to_str(item))

    def insert(self, index: int, item: Any):
        """
        Insert an item in the ``StringList``.

        Args:
            index:
                An integer index containing a position to insert at.

            item:
                A scalar that can be coerced into a string, or None.

        Returns:
            ``item`` is inserted at ``index`` in the current object.
        """
        super().insert(index, _coerce_to_str(item))

    def append(self, item: Any):
        """
        Append an item to the end of a ``StringList``.

        Args:
            item:
                A scalar that can be coerced into a string, or None.

        Returns:
            ``item`` is added to the end of the current object.
        """
        super().append(_coerce_to_str(item))

    def extend(self, iterable: Iterable):
        """
        Extend the end of a ``StringList`` with more items.

        Args:
            iterable: 
                Some iterable object where all values can be coerced to strings
                or are None.

        Returns:
            Items in ``iterable`` are added to the end of the current object.
        """
        new_it = iterable
        if not isinstance(iterable, type(self)):
            new_it = (_coerce_to_str(item) for item in iterable)
        super().extend(new_it)

    def __add__(self, other: list) -> "StringList":
        """
        Add a list to the right of a ``StringList``.

        Args:
            other:
                A list of items that can be coerced to strings or are None.

        Returns:
            A new ``StringList`` containing the concatenation of the
            current object's items and those of ``other``.
        """
        output = self.copy()
        output.extend(other)
        return output

    def __iadd__(self, other: list):
        """
        Extend an existing ``StringList`` with a new list.

        Args:
            other:
                A list of items that can be coerced to strings or are None.

        Returns:
            The current object is extended with the contents of ``other``.
        """
        self.extend(other)
        return self

    def copy(self) -> "StringList":
        """
        Make a copy of a ``StringList``.

        Returns:
            A new ``StringList`` with the same contents.
        """
        return StringList(self, coerce=False)
