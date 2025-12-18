from typing import Any, Iterable, Optional, Sequence, Union

from .named_list import NamedList
from .names import Names
from .normalize_subscript import SubscriptTypes


def _coerce_to_bool(x: Any):
    return None if x is None else bool(x)


class _SubscriptCoercer:
    """Coercer for subscript operations on BooleanList."""

    def __init__(self, data: Sequence) -> None:
        """Initialize the coercer.

        Args:
            data: Sequence of values to coerce.
        """
        self._data = data

    def __getitem__(self, index: int) -> Optional[bool]:
        """Get an item and coerce it to boolean.

        Args:
            index: Index of the item.

        Returns:
            Coerced boolean value.
        """
        return _coerce_to_bool(self._data[index])


class BooleanList(NamedList):
    """
    List of booleans. This mimics a regular Python list except that anything
    added to it will be coerced into a boolean. None values are also acceptable
    and are treated as missing booleans. The list may also be named (see
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
                Some iterable object where all values can be coerced to booleans
                or are None.

                Alternatively this may itself be None, which defaults to an empty list.

            names:
                Names for the list elements, defaults to an empty list.

            _validate:
                Internal use only.
        """
        if _validate:
            if data is not None:
                if isinstance(data, BooleanList):
                    data = data._data
                else:
                    if isinstance(data, NamedList):
                        data = data._data
                    original = data
                    data = list(_coerce_to_bool(item) for item in original)
        super().__init__(data, names, _validate=_validate)

    def set_value(
        self, index: Union[int, str], value: Any, in_place: bool = False
    ) -> "BooleanList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.set_value` after coercing ``value`` to a boolean."""
        return super().set_value(index, _coerce_to_bool(value), in_place=in_place)

    def set_slice(
        self, index: SubscriptTypes, value: Sequence, in_place: bool = False
    ) -> "BooleanList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.set_slice` after coercing ``value`` to booleans."""
        return super().set_slice(index, _SubscriptCoercer(value), in_place=in_place)

    def safe_insert(
        self, index: Union[int, str], value: Any, in_place: bool = False
    ) -> "BooleanList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_insert` after coercing ``value`` to a boolean."""
        return super().safe_insert(index, _coerce_to_bool(value), in_place=in_place)

    def safe_append(self, value: Any, in_place: bool = False) -> "BooleanList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_append` after coercing ``value`` to a boolean."""
        return super().safe_append(_coerce_to_bool(value), in_place=in_place)

    def safe_extend(self, other: Iterable, in_place: bool = True) -> "BooleanList":
        """Calls :py:meth:`~biocutils.NamedList.NamedList.safe_extend` after coercing elements of ``other`` to booleans."""
        return super().safe_extend(
            (_coerce_to_bool(y) for y in other), in_place=in_place
        )
