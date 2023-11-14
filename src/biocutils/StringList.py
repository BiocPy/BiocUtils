from typing import Any, Union, Optional
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
    Python list of strings. This is the same as a regular Python list except
    that anything added to it will be coerced into a string. None values are
    also acceptable and are treated as missing strings.
    """

    def __init__(self, iterable: Optional[Iterable] = None, names: Optional[Names] = None, coerce: bool = True):
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
            if coerce and not isinstance(iterable, type(self)):
                iterable = (_coerce_to_str(item) for item in iterable)
        super().__init__(iterable, names)

    def set_slice(self, index: Union[int, str, slice], value: Sequence, in_place: bool = False, normalize: bool = True) -> "NamedList":
        return super().set_slice(index, _SubscriptCoercer(value), in_place=in_place, normalize=normalize)

    def safe_insert(self, index: Union[int, str], item: Any, in_place: bool = False) -> "NamedList":
        return super().safe_insert(index, _coerce_to_str(item), in_place=in_place) 

    def safe_append(self, item: Any, in_place: bool = False) -> "NamedList":
        return super().safe_append(_coerce_to_str(item), in_place=in_place)

    def safe_extend(self, other: Iterable, in_place: bool = True) -> "NamedList":
        return super().safe_extend(_coerce_to_str(y) for y in other, in_place=in_place)
