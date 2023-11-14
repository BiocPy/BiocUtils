from copy import copy, deepcopy
from typing import List, Sequence, Union, Optional
from warnings import warn
import numpy

from .StringList import StringList
from .Names import Names, _name_to_position, _sanitize_names, _combine_names
from .match import match
from .factorize import factorize
from .normalize_subscript import normalize_subscript, SubscriptTypes
from .is_missing_scalar import is_missing_scalar
from .print_truncated import print_truncated_list

from .subset_sequence import subset_sequence
from .assign_sequence import assign_sequence
from .combine_sequences import combine_sequences
from .is_list_of_type import is_list_of_type


def _sanitize_codes(codes: Sequence[int], num_levels: int) -> numpy.ndarray:
    if not isinstance(codes, numpy.ndarray):
        replacement = numpy.ndarray(len(codes), dtype=numpy.min_scalar_type(-num_levels)) # get a signed type.
        for i, x in enumerate(codes):
            if is_missing_scalar(x) or x < 0:
                replacement[i] = -1
            else:
                replacement[i] = x
        codes = replacement
    else:
        if len(codes.shape) != 1:
            raise ValueError("'codes' should be a 1-dimensional array")
        if not numpy.issubdtype(codes.dtype, numpy.signedinteger): # force it to be signed.
            codes = codes.astype(numpy.min_scalar_type(-num_levels))

    for x in codes:
        if x < -1 or x >= num_levels:
            raise ValueError("all entries of 'codes' should refer to an entry of 'levels'")

    return codes


def _sanitize_levels(levels: Sequence[str], check: bool = True) -> StringList:
    if not isinstance(levels, StringList):
        levels = StringList(levels)
    if levels.get_names() is not None:
        levels = levels.set_names(None)

    if check:
        if any(x is None for x in levels):
            raise TypeError("all entries of 'levels' should be non-missing")
        if len(set(levels)) < len(levels):
            raise ValueError("all entries of 'levels' should be unique")

    return levels


class Factor:
    """Factor class, equivalent to R's ``factor``.

    This is a vector of integer codes, each of which is an index into a list of
    unique strings. The aim is to encode a list of strings as integers for
    easier numerical analysis.
    """

    def __init__(self, codes: Sequence[int], levels: Sequence[str], ordered: bool = False, names: Optional[Names] = None, _validate: bool = True):
        """Initialize a Factor object.

        Args:
            codes:
                Sequence of codes. Each valid code should be a non-negative
                integer that refers to an entry ``levels``. Codes may be
                negative or correspond to a missing scalar (as defined by
                :py:meth:`~biocutils.is_missing_scalar.is_missing_scalar`),
                in which case they are assumed to represent missing values.

            levels:
                List of levels containing unique strings.

            ordered:
                Whether the levels are ordered.

            names:
                List of names. This should have same length as ``codes``.
                Alternatively None, if the factor has no names yet.

            validate:
                Whether to validate the arguments. Internal use only.
        """
        if _validate:
            levels = _sanitize_levels(levels)
            codes = _sanitize_codes(codes, len(levels))
            names = _sanitize_names(names, len(codes))

        self._codes = codes
        self._levels = levels
        self._ordered = bool(ordered)
        self._names = names

    ##################################
    #####>>>> Simple getters <<<<#####
    ##################################

    def _define_output(self, in_place: bool) -> "Factor":
        if in_place:
            return self
        else:
            return copy(self)

    def get_codes(self) -> numpy.ndarray:
        """
        Returns:
            Array of integer codes, used as indices into the levels from
            :py:attr:`~get_levels`. Missing values are marked with -1.
        """
        return self._codes

    @property
    def codes(self) -> numpy.ndarray:
        """Alias for :py:attr:`~get_codes`."""
        return self.get_codes()

    def set_codes(self, codes: Sequence[int], in_place: bool = False) -> "Factor":
        """
        Args:
            codes:
                Integer codes referencing the factor levels. This should
                have the same length as the current object.

            in_place:
                Whether to modify this object in-place.

        Returns:
            A modified ``Factor`` object with the new codes, either as a 
            new object or as a reference to the current object.
        """
        output = self._define_output(in_place)
        if len(codes) != len(self):
            raise ValueError("length of 'codes' should be equal to that of the current object")
        output._codes = _sanitize_codes(codes, len(self._levels))
        return output

    def get_levels(self) -> StringList:
        """
        Returns:
            List of strings containing the factor levels.
        """
        return self._levels

    @property
    def levels(self) -> StringList:
        """Alias for :py:attr:`~get_levels`."""
        return self.get_levels()

    def get_ordered(self) -> bool:
        """
        Returns:
            True if the levels are ordered, otherwise False.
        """
        return self._ordered

    @property
    def ordered(self) -> bool:
        """Alias for :py:attr:`~get_ordered`."""
        return self.get_ordered()

    def set_ordered(self, ordered: bool, in_place: bool = False) -> "Factor":
        """
        Args:
            ordered:
                Whether to treat the levels as being ordered.

            in_place:
                Whether to modify this object in-place.

        Returns:
            A modified ``Factor`` object with the new ordered status, either as
            a new object or as a reference to the current object.
        """
        output = self._define_output(in_place)
        output._ordered = bool(ordered)
        return output

    def get_names(self) -> Names:
        """
        Returns:
            Names for the factor elements.
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
            A modified ``Factor`` with the new names, either as a new object or
            as a reference to the current object.
        """
        output = self._define_output(in_place)
        output._names = _sanitize_names(names, len(self)) 
        return output

    #################################
    #####>>>> Miscellaneous <<<<#####
    #################################

    def __len__(self) -> int:
        """
        Returns:
            Length of the factor in terms of the number of codes.
        """
        return len(self._codes)

    def __repr__(self) -> str:
        """
        Returns:
            A stringified representation of this object.
        """
        tmp = "Factor(codes=" + print_truncated_list(self._codes) + ", levels=" + print_truncated_list(self._levels)
        if self._ordered:
            tmp += ", ordered=True"
        if self._names:
            tmp += ", names=" + print_truncated_list(self._names)
        tmp += ")"
        return tmp

    def __str__(self) -> str:
        """
        Returns:
            A pretty-printed representation of this object.
        """
        message = "Factor of length " + str(len(self._codes)) + " with " + str(len(self._levels)) + " level"
        if len(self._levels) != 0:
            message += "s"
        message += "\n"
        message += "values: " + print_truncated_list(self._codes, transform=lambda i: self._levels[i], include_brackets=False) + "\n"
        if self._names is not None:
            message += "names: " + print_truncated_list(self._names, transform=lambda x: x, include_brackets=False) + "\n"
        message += "levels: " + print_truncated_list(self._levels, transform=lambda x: x, include_brackets=False) + "\n"
        message += "ordered: " + str(self._ordered)
        return message

    ###########################
    #####>>>> Slicing <<<<#####
    ###########################

    def get_value(self, index: Union[str, int]) -> Union[str, None]:
        """
        Args:
            index:
                Integer index of the element to obtain. Alternatively, a string
                containing the name of the element, using the first occurrence
                if duplicate names are present. 

        Returns:
            The factor level for the code at the specified position, or None if
            the entry is missing.
        """
        if isinstance(index, str):
            index = _name_to_position(self._names, index)
        i = self._codes[index]
        if i < 0:
            return None
        return self._levels[i]

    def get_slice(self, index: SubscriptTypes) -> "Factor":
        """
        Args:
            index:
                Subset of elements to obtain, see
                :py:func:`~biocutils.normalize_subscript.normalize_subscript`
                for details. Strings are matched to names in the current
                object, using the first occurrence if duplicate names are
                present.  Scalars are treated as length-1 sequences.

        Returns:
            A ``Factor`` is returned containing the specified subset.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        output = copy(self)
        output._codes = self._codes[index]
        if output._names is not None:
            output._names = subset_sequence(self._names, index)
        return output

    def __getitem__(self, index: SubscriptTypes) -> Union[str, "Factor"]:
        """
        If ``index`` is a scalar, this is an alias for :py:attr:`~get_value`.

        If ``index`` is a sequence, this is an alias for :py:attr:`~get_slice`.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            return self.get_value(index[0])
        else:
            return self.get_slice(index)

    def set_value(self, index: Union[str, int], value: Union[str, None], in_place: bool = False) -> "Factor":
        """
        Args:
            index:
                Integer index of the element to replace. Alternatively, a string
                containing the name of the element, using the first occurrence
                if duplicate names are present. 

            value:
                Replacement value. This should be a string corresponding to a
                factor level, or None if missing.

            in_place:
                Whether to perform the modification in place.

        Returns:
            A ``Factor`` object with the modified entry at ``index``. This is either
            a new object or a reference to the current object.
        """
        if in_place:
            output = self
        else:
            output = copy(self)
            output._codes = copy(self._codes)

        if isinstance(index, str):
            index = _name_to_position(self._names, index)

        if value is None:
            output._codes[index] = -1
            return output

        for i, l in enumerate(output._levels):
            if l == value:
                output._codes[index] = i
                return output

        raise IndexError("failed to find level '" + str(value) + "'")

    def set_slice(self, index: SubscriptTypes, value: "Factor", in_place: bool = False):
        """
        Replace items in the ``Factor`` list.  The ``index`` elements in the
        current object are replaced with the corresponding values in ``value``.
        This is performed by finding the level for each entry of the
        replacement ``value``, matching it to a level in the current object,
        and replacing the entry of ``codes`` with the code of the matched
        level. If there is no matching level, a missing value is inserted.

        Args:
            index: 
                Subset of elements to replace, see
                :py:func:`~biocutils.normalize_subscript.normalize_subscript`
                for details. Strings are matched to names in the current
                object, using the first occurrence if duplicate names are
                present. Scalars are treated as length-1 sequences.

            value: 
                A ``Factor`` of the same length containing the replacement values.

            in_place:
                Whether the replacement should be performed in place.

        Returns:
            A ``Factor`` object with values at ``index`` replaced by ``value``.
            This is either a new object or a reference to the current object,
            depending on ``in_place``.
        """
        if in_place:
            output = self
        else:
            output = copy(self)
            output._codes = copy(self._codes)

        new_codes = output._codes

        index, scalar = normalize_subscript(index, len(self), self._names)
        if self._levels == value._levels:
            for i, x in enumerate(index):
                new_codes[x] = value._codes[i]
        else:
            mapping = match(value._levels, self._levels)
            for i, x in enumerate(index):
                v = value._codes[i]
                if v >= 0:
                    new_codes[x] = mapping[v]
                else:
                    new_codes[x] = -1

        return output

    def __setitem__(self, index: SubscriptTypes, value: Union[str, "Factor"]):
        """
        If ``index`` is a scalar, this is an alias for :py:attr:`~set_value`.

        If ``index`` is a sequence, this is an alias for :py:attr:`~set_slice`.
        """
        index, scalar = normalize_subscript(index, len(self), self._names)
        if scalar:
            self.set_value(index, value, in_place=True)
        else:
            self.set_slice(index, value, in_place=True)

    #################################
    #####>>>> Level setting <<<<#####
    #################################

    def drop_unused_levels(self, in_place: bool = False) -> "Factor":
        """Drop unused levels.

        Args:
            in_place: Whether to perform this modification in-place.

        Returns:
            If ``in_place = False``, returns same type as caller (a new ``Factor`` object)
            where all unused levels have been removed.

            If ``in_place = True``, unused levels are removed from the
            current object; a reference to the current object is returned.
        """
        if in_place:
            output = self
        else:
            output = copy(self)
            output._codes = copy(self._codes)

        in_use = [False] * len(self._levels)
        for x in self._codes:
            if x >= 0:
                in_use[x] = True

        new_levels = StringList([])
        reindex = [-1] * len(in_use)
        for i, x in enumerate(in_use):
            if x:
                reindex[i] = len(new_levels)
                new_levels.append(self._levels[i])

        new_codes = output._codes
        for i, x in enumerate(self._codes):
            if x >= 0:
                new_codes[i] = reindex[x]

        output._levels = new_levels
        return output

    def set_levels(self, levels: Union[str, Sequence[str]], in_place: bool = False) -> "Factor":
        """Set or replace levels.

        Args:
            levels:
                A sequence of replacement levels. These should be unique
                strings with no missing values.

                Alternatively a single string containing an existing level in
                this object. The new levels are defined as a permutation of the
                existing levels where the provided string is now the first
                level. The order of all other levels is preserved.

            in_place:
                Whether to perform this modification in-place.

        Returns:
            If ``in_place = False``, returns same type as caller (a new
            ``Factor`` object) where the levels have been replaced. This will
            automatically update the codes so that they still refer to the same
            string in the new ``levels``. If a code refers to a level that is
            not present in the new ``levels``, it is replaced with None.

            If ``in_place = True``, the levels are replaced in the current
            object, and a reference to the current object is returned.
        """
        if in_place:
            output = self
        else:
            output = copy(self)
            output._codes = copy(self._codes)

        lmapping = {}
        if isinstance(levels, str):
            new_levels = StringList([levels])
            for x in self._levels:
                if x == levels:
                    lmapping[x] = 0
                else:
                    lmapping[x] = len(new_levels)
                    new_levels.append(x)
            if levels not in lmapping:
                raise ValueError(
                    "string 'levels' should already be present among object levels"
                )
        else:
            new_levels = levels
            if not isinstance(new_levels, StringList):
                new_levels = StringList(levels)
            for i, x in enumerate(new_levels):
                if x is None:
                    raise TypeError("all entries of 'levels' should be non-missing")
                if x in lmapping:
                    raise ValueError("all entries of 'levels' should be unique")
                lmapping[x] = i

        mapping = [-1] * len(self._levels)
        for i, x in enumerate(self._levels):
            if x in lmapping:
                mapping[i] = lmapping[x]

        new_codes = output._codes
        for i, x in enumerate(new_codes):
            if x >= 0:
                new_codes[i] = mapping[x]
            else:
                new_codes[i] = -1

        output._levels = new_levels
        return output

    ###########################
    #####>>>> Copying <<<<#####
    ###########################

    def __copy__(self) -> "Factor":
        """
        Returns:
            A shallow copy of the ``Factor`` object.
        """
        return type(self)(
            self._codes, 
            levels=self._levels, 
            ordered=self._ordered, 
            names=self._names, 
            _validate=False,
        )

    def __deepcopy__(self, memo) -> "Factor":
        """
        Returns:
            A deep copy of the ``Factor`` object.
        """
        return type(self)(
            deepcopy(self._codes, memo),
            levels=deepcopy(self._levels, memo),
            ordered=self._ordered,
            names=deepcopy(self._names, memo),
            _validate=False,
        )

    #############################
    #####>>>> Coercions <<<<#####
    #############################

    def to_pandas(self):
        """Coerce to :py:class:`~pandas.Categorical` object.

        Returns:
            Categorical: A :py:class:`~pandas.Categorical` object.
        """
        from pandas import Categorical
        return Categorical(
            values=[self._levels[c] for c in self._codes],
            ordered=self._ordered,
        )

    @staticmethod
    def from_sequence(x: Sequence[str], levels: Optional[Sequence[str]] = None, sort_levels: bool = True, ordered: bool = False) -> "Factor":
        """Convert a sequence of hashable values into a factor.

        Args:
            x: 
                A sequence of strings. Any value may be None to indicate
                missingness.

            levels:
                Sequence of reference levels, against which the entries in ``x`` are compared.
                If None, this defaults to all unique values of ``x``.

            sort_levels:
                Whether to sort the automatically-determined levels. If False,
                the levels are kept in order of their appearance in ``x``.  Not
                used if ``levels`` is explicitly supplied.

            ordered (bool):
                Whether the levels should be assumed to be ordered.  Note that
                this refers to their importance and has nothing to do with
                their sorting order or with the setting of ``sort_levels``.

        Returns:
            A ``Factor`` object.
        """
        levels, indices = factorize(x, levels=levels, sort_levels=sort_levels)
        return Factor(indices, levels=levels, ordered=ordered)


@subset_sequence.register
def _subset_sequence_Factor(x: Factor, indices: Sequence[int]) -> Factor:
    return x.get_slice(indices)


@assign_sequence.register
def _assign_sequence_Factor(x: Factor, indices: Sequence[int], other: Factor) -> Factor:
    return x.set_slice(indices, other)


@combine_sequences.register(Factor)
def _combine_factors(*x: Factor):
    if not is_list_of_type(x, Factor):
        raise ValueError("all elements to `combine` must be `Factor` objects")

    first = x[0]
    first_levels = first._levels
    all_same = True
    for f in x[1:]:
        cur_levels = f._levels
        if cur_levels != first_levels or f._ordered != first._ordered:
            all_same = False
            break

    new_codes = []
    if all_same:
        for f in x:
            new_codes.append(f._codes)
        new_levels = first._levels
        new_ordered = first._ordered
    else:
        all_levels_map = {}
        new_levels = StringList()
        for f in x:
            mapping = []
            for i, y in enumerate(f._levels):
                if y not in all_levels_map:
                    all_levels_map[y] = len(new_levels)
                    new_levels.append(y)
                mapping.append(all_levels_map[y])

            curout = numpy.ndarray(len(f), dtype=numpy.min_scalar_type(-len(new_levels)))
            for i, j in enumerate(f._codes):
                if j < 0:
                    curout[i] = j
                else:
                    curout[i] = mapping[j]
            new_codes.append(curout)
        new_ordered = False

    return type(x[0])(
        codes=combine_sequences(*new_codes), 
        levels=new_levels, 
        ordered=new_ordered, 
        names=_combine_names(*x, get_names=lambda x : x.get_names()),
        _validate=False,
    )
