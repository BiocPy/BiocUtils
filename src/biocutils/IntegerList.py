from typing import Any, Iterable, Optional, Sequence, Union

from .NamedList import NamedList
from .Names import Names
from .normalize_subscript import SubscriptTypes


def _coerce_to_int(x: Any):
    if x is None:
        return None
    try:
        return int(x)
    except:
        return None


class _SubscriptCoercer:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        return _coerce_to_int(self._data[index])


class IntegerList(NamedList):
    """
    List of integers. This mimics a regular Python list except that anything
    added to it will be coerced into a integer. None values are also acceptable
    and are treated as missing integers. The list may also be named (see
    :py:class:`~NamedList`), which provides some dictionary-like functionality.
    """

    def __init__(
        self,
        data: Optional[Iterable] = None,
        names: Optional[Names] = None,
        _validate: bool = True,
    ):
        """
        Args:
           data:
                Some iterable object where all values can be coerced to integers
                or are None.

                Alternatively this may itself be None, which defaults to an empty list.

            names:
                Names for the list elements, defaults to an empty list.

            _validate:
                Internal use only.
        """
        if _validate:
            if data is not None:
                if isinstance(data, IntegerList):
                    data = data._data
                else:
                    if isinstance(data, NamedList):
                        data = data._data
                    original = data
                    data = list(_coerce_to_int(item) for item in original)
        super().__init__(data, names, _validate=_validate)

    def set_value(
        self, index: Union[int, str], value: Any, in_place: bool = False
    ) -> "IntegerList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.set_value` after coercing ``value`` to a integer."""
        return super().set_value(index, _coerce_to_int(value), in_place=in_place)

    def set_slice(
        self, index: SubscriptTypes, value: Sequence, in_place: bool = False
    ) -> "IntegerList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.set_slice` after coercing ``value`` to integers."""
        return super().set_slice(index, _SubscriptCoercer(value), in_place=in_place)

    def safe_insert(
        self, index: Union[int, str], value: Any, in_place: bool = False
    ) -> "IntegerList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_insert` after coercing ``value`` to a integer."""
        return super().safe_insert(index, _coerce_to_int(value), in_place=in_place)

    def safe_append(self, value: Any, in_place: bool = False) -> "IntegerList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_append` after coercing ``value`` to a integer."""
        return super().safe_append(_coerce_to_int(value), in_place=in_place)

    def safe_extend(self, other: Iterable, in_place: bool = True) -> "IntegerList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_extend` after coercing elements of ``other`` to integers."""
        return super().safe_extend(
            (_coerce_to_int(y) for y in other), in_place=in_place
        )
