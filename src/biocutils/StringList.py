from typing import Any, Union, Optional, Sequence, Iterable
from collections.abc import Iterable

from .Names import Names
from .NamedList import NamedList
from .subset_sequence import subset_sequence
from .combine_sequences import combine_sequences
from .assign_sequence import assign_sequence


def _coerce_to_str(x: Any) -> bool:
    return None if x is None else str(x)


class _SubscriptCoercer:
    def __init__(self, data):
        self._data = data
    def __getitem__(self, index):
        return _coerce_to_str(self._data[index])


class StringList(NamedList):
    """
    List of strings. This mimics a regular Python list except that anything
    added to it will be coerced into a string. None values are also acceptable
    and are treated as missing strings. The list may also be named (see
    :py:class:`~NamedList`), which provides some dictionary-like functionality.
    """

    def __init__(self, data: Optional[Iterable] = None, names: Optional[Names] = None, _validate: bool = True):
        """
        Args:
           data: 
                Some iterable object where all values can be coerced to strings
                or are None. 

                Alternatively this may itself be None, which defaults to an empty list.

            names:
                Names for the list elements, defaults to an empty list.

            _validate:
                Internal use only.
        """
        if _validate:
            if data is not None:
                if isinstance(data, StringList):
                    data = data._data
                else:
                    if isinstance(data, NamedList):
                        data = data._data
                    original = data
                    data = list(_coerce_to_str(item) for item in original)
        super().__init__(data, names, _validate=_validate)

    def set_value(self, index: Union[int, str], value: Any, in_place: bool = False) -> "StringList":
        """Calls :py:meth:`~NamedList.NamedList.set_value` after coercing ``value`` to a string."""
        return super().set_value(index, _coerce_to_str(value), in_place=in_place) 

    def set_slice(self, index: Union[int, str, slice], value: Sequence, in_place: bool = False) -> "StringList":
        """Calls :py:meth:`~NamedList.NamedList.set_slice` after coercing ``value`` to strings."""
        return super().set_slice(index, _SubscriptCoercer(value), in_place=in_place) 

    def safe_insert(self, index: Union[int, str], value: Any, in_place: bool = False) -> "StringList":
        """Calls :py:meth:`~NamedList.NamedList.safe_insert` after coercing ``value`` to a string."""
        return super().safe_insert(index, _coerce_to_str(value), in_place=in_place) 

    def safe_append(self, value: Any, in_place: bool = False) -> "StringList":
        """Calls :py:meth:`~NamedList.NamedList.safe_append` after coercing ``value`` to a string."""
        return super().safe_append(_coerce_to_str(value), in_place=in_place)

    def safe_extend(self, other: Iterable, in_place: bool = True) -> "StringList":
        """Calls :py:meth:`~NamedList.NamedList.safe_extend` after coercing elements of ``other`` to strings."""
        return super().safe_extend((_coerce_to_str(y) for y in other), in_place=in_place)
