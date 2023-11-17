from copy import deepcopy
from typing import Any, Dict, Iterable, Optional, Sequence, Union

from .assign_sequence import assign_sequence
from .combine_sequences import combine_sequences
from .Names import Names, _name_to_position, _sanitize_names
from .normalize_subscript import (
    NormalizedSubscript,
    SubscriptTypes,
    normalize_subscript,
)
from .subset_sequence import subset_sequence


class NamedList:
    """
    A list-like object that could have names for each element, equivalent to R's
    named list. This combines list and dictionary functionality, e.g., it can
    be indexed by position or slices (list) but also by name (dictionary).
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
                Sequence of data values.

                Alternatively None, for an empty list.

            names:
                List of names. This should have same length as ``data``.
                Alternatively None, if the list has no names yet.

            _validate:
                Internal use only.
        """
        if _validate:
            if data is None:
                data = []
            elif isinstance(data, NamedList):
                data = data._data
            elif not isinstance(data, list):
                data = list(data)
            names = _sanitize_names(names, len(data))
        self._data = data
        self._names = names

    ###################################
    #####>>>> Bits and pieces <<<<#####
    ###################################

    def __len__(self) -> int:
        """
        Returns:
            Length of the list.
        """
        return len(self._data)

    def __iter__(self) -> "list_iterator":
        """
        Returns:
            An iterator on the underlying list of data.
        """
        return iter(self._data)

    def __repr__(self) -> str:
        """
        Returns:
            Representation of the current list.
        """
        message = type(self).__name__ + "(data=" + repr(self._data)
        if self._names is not None:
            message += ", names=" + repr(self._names)
        message += ")"
        return message

    def __str__(self) -> str:
        """
        Returns:
            Pretty-printed representation of the current list, along with its
            names if any exist.
        """
        if self._names is not None:
            return (
                "["
                + ", ".join(
                    repr(self._names[i]) + "=" + repr(x)
                    for i, x in enumerate(self._data)
                )
                + "]"
            )
        else:
            return repr(self._data)

    def __eq__(self, other: "NamedList") -> bool:
        """
        Args:
            other: Another ``NamedList``.

        Returns:
            Whether the current object is equal to ``other``, i.e.,
            same data and names.
        """
        return self._data == other._data and self._names == other._names

    #################################
    #####>>>> Get/set names <<<<#####
    #################################

    def get_names(self) -> Names:
        """
        Returns:
            Names for the list elements.
        """
        return self._names

    @property
    def names(self) -> Names:
        """Alias for :py:meth:`~get_names`."""
        return self.get_names()

    def _shallow_copy(self):
        return type(self)(self._data, self._names, _validate=False)

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
            output = self._shallow_copy()
        output._names = _sanitize_names(names, len(self))
        return output

    #################################
    #####>>>> Get/set items <<<<#####
    #################################

    def get_value(self, index: Union[str, int]) -> Any:
        """
        Args:
            index:
                Integer index of the element to obtain. Alternatively, a string
                containing the name of the element, using the first occurrence
                if duplicate names are present.

        Returns:
            The value at the specified position (or with the specified name).
        """
        if isinstance(index, str):
            index = _name_to_position(self._names, index)
        return self._data[index]

    def get_slice(self, index: SubscriptTypes) -> "NamedList":
        """
        Args:
            index:
                Subset of elements to obtain, see
                :py:func:`~biocutils.normalize_subscript.normalize_subscript`
                for details. Strings are matched to names in the current
                object, using the first occurrence if duplicate names are
                present. Scalars are treated as length-1 sequences.

        Returns:
            A ``NamedList`` is returned containing the specified subset.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        outdata = subset_sequence(self._data, index)
        outnames = None
        if self._names is not None:
            outnames = subset_sequence(self._names, index)
        return type(self)(outdata, outnames, _validate=False)

    def __getitem__(self, index: SubscriptTypes) -> Union["NamedList", Any]:
        """
        If ``index`` is a scalar, this is an alias for :py:meth:`~get_value`.

        If ``index`` is a sequence, this is an alias for :py:meth:`~get_slice`.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            return self.get_value(index[0])
        else:
            return self.get_slice(NormalizedSubscript(index))

    def set_value(
        self, index: Union[str, int], value: Any, in_place: bool = False
    ) -> "NamedList":
        """
        Args:
            index:
                Integer index of the element to obtain. Alternatively, a string
                containing the name of the element; we consider the first
                occurrence of the name if duplicates are present.

            value:
                Replacement value of the list element.

            in_place:
                Whether to perform the replacement in place.

        Returns:
            A ``NamedList`` is returned after the value at the specified position
            (or with the specified name) is replaced. If ``in_place = False``, this
            is a new object, otherwise it is a reference to the current object.

            If ``index`` is a name that does not already exist in the current
            object, ``value`` is added to the end of the list, and the
            ``index`` is added as a new name.
        """
        if in_place:
            output = self
        else:
            output = self._shallow_copy()
            output._data = output._data.copy()

        if isinstance(index, str):
            if self._names is not None:
                i = self._names.map(index)
                if i < 0:
                    output._names = self._names.copy()
                    output._names.append(index)
                    output._data.append(value)
                else:
                    output._data[i] = value
            else:
                output._names = Names([""] * len(output._data))
                output._names.append(index)
                output._data.append(value)
        else:
            output._data[index] = value

        return output

    def set_slice(
        self, index: SubscriptTypes, value: Sequence, in_place: bool = False
    ) -> "NamedList":
        """
        Args:
            index:
                Subset of elements to replace, see
                :py:func:`~biocutils.normalize_subscript.normalize_subscript`
                for details. Strings are matched to names in the current
                object, using the first occurrence if duplicate names are
                present. Scalars are treated as length-1 sequences.

            value:
                If ``index`` is a sequence, a sequence of the same length
                containing values to be set at the positions in ``index``.

                If ``index`` is a scalar, any object to be used as the
                replacement value for the position at ``index``.

            in_place:
                Whether to perform the replacement in place.

        Returns:
            A ``NamedList`` where the entries at ``index`` are replaced with
            the contents of ``value``. If ``in_place = False``, this is a new
            object, otherwise it is a reference to the current object.

            Unlike :py:meth:`~set_value`, this will not add new elements if
            ``index`` contains names that do not already exist in the object;
            a missing name error is raised instead.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        if in_place:
            output = self
        else:
            output = self._shallow_copy()
            output._data = output._data.copy()
        if scalar:
            output._data[index[0]] = value
        else:
            for i, j in enumerate(index):
                output._data[j] = value[i]
        return output

    def __setitem__(self, index: SubscriptTypes, value: Any):
        """
        If ``index`` is a scalar, this is an alias for :py:meth:`~set_value`
        with ``in_place = True``.

        If ``index`` is a sequence, this is an alias for :py:meth:`~set_slice`
        with ``in_place = True``.
        """
        if isinstance(index, str):
            self.set_value(index, value, in_place=True)
        else:
            index, scalar = normalize_subscript(index, len(self), self._names)
            if scalar:
                self.set_value(index[0], value, in_place=True)
            else:
                self.set_slice(NormalizedSubscript(index), value, in_place=True)

    ################################
    #####>>>> List methods <<<<#####
    ################################

    def _define_output(self, in_place: bool) -> "NamedList":
        if in_place:
            return self
        else:
            return self.copy()

    def safe_insert(
        self, index: Union[int, str], value: Any, in_place: bool = False
    ) -> "NamedList":
        """
        Args:
            index:
                An integer index containing a position to insert at.
                Alternatively, the name of the value to insert at (the first
                occurrence of each name is used).

            value:
                A value to be inserted into the current object.

            in_place:
                Whether to modify the current object in place.

        Returns:
            A ``NamedList`` where ``value`` is inserted at ``index``. This is a
            new object if ``in_place = False``, otherwise it is a reference to
            the current object. If names are present in the current object, the
            newly inserted element's name is set to an empty string.
        """
        output = self._define_output(in_place)
        if isinstance(index, str):
            index = _name_to_position(self._names, index)
        output._data.insert(index, value)
        if output._names is not None:
            output._names.insert(index, "")
        return output

    def insert(self, index: Union[int, str], value: Any):
        """Alias for :py:meth:`~safe_insert` with ``in_place = True``."""
        self.safe_insert(index, value, in_place=True)

    def safe_append(self, value: Any, in_place: bool = False) -> "NamedList":
        """
        Args:
            value:
                Any value.

            in_place:
                Whether to perform the modification in place.

        Returns:
            A ``NamedList`` where ``value`` is added to the end. If ``in_place
            = False``, this is a new object, otherwise it is a reference to the
            current object. If names are present in the current object, the
            newly added element has its name set to an empty string.
        """
        output = self._define_output(in_place)
        output._data.append(value)
        if output._names is not None:
            output._names.append("")
        return output

    def append(self, value: Any):
        """Alias for :py:meth:`~safe_append` with ``in_place = True``."""
        self.safe_append(value, in_place=True)

    def safe_extend(self, other: Iterable, in_place: bool = False) -> "NamedList":
        """
        Args:
            other:
                Some iterable object. If this is a ``NamedList``, its names are
                used to extend the names of the current object; otherwise the
                extended names are set to empty strings.

            in_place:
                Whether to perform the modification in place.

        Returns:
            A ``NamedList`` where items in ``other`` are added to the end. If
            ``in_place = False``, this is a new object, otherwise a reference
            to the current object is returned.
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
        """Alias for :py:meth:`~safe_extend` with ``in_place = True``."""
        self.safe_extend(other, in_place=True)

    def __add__(self, other: list) -> "NamedList":
        """Alias for :py:meth:`~safe_extend`."""
        return self.safe_extend(other)

    def __iadd__(self, other: list):
        """Alias for :py:meth:`~extend`, returning a reference to the current
        object after the in-place modification."""
        self.extend(other)
        return self

    ################################
    #####>>>> Copy methods <<<<#####
    ################################

    def copy(self) -> "NamedList":
        """
        Returns:
            A shallow copy of a ``NamedList`` with the same contents.  This
            will copy the underlying list (and names, if any exist) so that any
            in-place operations like :py:meth:`~append`, etc., on the new
            object will not change the original object.
        """
        newnames = self._names
        if newnames is not None:
            newnames = newnames.copy()
        return type(self)(self._data.copy(), names=newnames, _validate=False)

    def __copy__(self) -> "NamedList":
        """Alias for :py:meth:`~copy`."""
        return self.copy()

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
        return type(self)(
            deepcopy(self._data, memo, _nil),
            names=deepcopy(self._names, memo, _nil),
            _validate=False,
        )

    ############################
    #####>>>> Coercion <<<<#####
    ############################

    def as_list(self) -> list:
        """
        Returns:
            The underlying list of elements.
        """
        return self._data

    def as_dict(self) -> Dict[str, Any]:
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
    def from_list(x: list) -> "NamedList":
        """
        Args:
            x: List of data elements.

        Returns:
            A ``NamedList`` instance with the contents of ``x`` and no names.
        """
        return NamedList(x)

    @staticmethod
    def from_dict(x: dict) -> "NamedList":
        """
        Args:
            x: Dictionary where keys are strings (or can be coerced to them).

        Returns:
            A ``NamedList`` instance where the list elements are the values of
            ``x`` and the names are the stringified keys.
        """
        return NamedList(list(x.values()), names=Names(str(y) for y in x.keys()))


@subset_sequence.register
def _subset_sequence_NamedList(x: NamedList, indices: Sequence[int]) -> NamedList:
    return x.get_slice(NormalizedSubscript(indices))


@combine_sequences.register
def _combine_sequences_NamedList(*x: NamedList) -> NamedList:
    output = x[0].copy()
    for i in range(1, len(x)):
        output.extend(x[i])
    return output


@assign_sequence.register
def _assign_sequence_NamedList(
    x: NamedList, indices: Sequence[int], other: Sequence
) -> NamedList:
    if isinstance(other, NamedList):
        # Do NOT set the names if 'other' is a NamedList. Names don't change
        # during assignment/setting operations, as a matter of policy. This is
        # for simplicity, efficiency (as the Names don't need to be reindexed)
        # but mainly because 'indices' could have been derived from a sequence
        # of names, and it would be weird for the same sequence of names to
        # suddently become an invalid indexing vector after an assignment.
        other = other._data
    return type(x)(
        assign_sequence(x._data, NormalizedSubscript(indices), other), names=x._names
    )
