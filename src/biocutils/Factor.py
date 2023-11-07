from copy import deepcopy
from typing import List, Sequence, Union
from warnings import warn
import numpy

from .match import match
from .factorize import factorize
from .print_truncated_list import print_truncated_list


def _check_levels_type(levels: numpy.ndarray):
    if not issubdtype(levels.dtype, numpy.str_):
        raise TypeError("all entries of 'levels' should be strings")
    if numpy.ma.is_masked(levels):
        raise TypeError("all entries of 'levels' should be non-missing")
    if len(levels.shape) != 1:
        raise TypeError("'codes' should be a 1-dimensional array")


class Factor:
    """Factor class, equivalent to R's ``factor``.

    This is a vector of integer codes, each of which is an index into a list of
    unique strings. The aim is to encode a list of strings as integers for
    easier numerical analysis.
    """

    def __init__(self, codes: Sequence[int], levels: Sequence[str], ordered: bool = False, validate: bool = True):
        """Initialize a Factor object.

        Args:
            codes:
                Sequence of codes. Each value should be a non-negative integer
                that refers to an entry ``levels``. Negative or None entries
                are assumed to refer to missing values.

            levels:
                List of levels containing unique strings.

            ordered:
                Whether the levels are ordered.

            validate:
                Whether to validate the arguments. Internal use only.
        """
        if not isinstance(codes, numpy.ndarray):
            replacement = numpy.ndarray(len(levels), dtype=numpy.min_scalar_type(-len(levels))) # get a signed type.
            for i, x in enumerate(codes):
                if x < 0 or x is None or numpy.ma.is_masked(x):
                    replacement[i] = -1
                else:
                    replacement[i] = x
            codes = replacement
        self._codes = codes

        if not isinstance(levels, numpy.ndarray):
            levels = numpy.array(levels, dtype=str)
        self._levels = levels

        self._ordered = bool(ordered)

        if validate:
            if not issubdtype(self._codes.dtype, numpy.signedinteger):
                raise TypeError("all entries of 'codes' should be signed integers")
            if len(self._codes.shape) != 1:
                raise TypeError("'codes' should be a 1-dimensional array")

            _check_levels_type(self._levels)

            for x in codes:
                if x >= len(self._levels):
                    raise ValueError("all entries of 'codes' should refer to an entry of 'levels'")
                else if 

            if len(set(self._levels)) < len(self._levels):
                raise ValueError("all entries of 'levels' should be unique")

    def get_codes(self) -> numpy.ndarray:
        """
        Returns:
            Array of integer codes, used as indices into the levels from
            :py:attr:`~get_levels`. A masked array may also be returned if
            any of the entries are missing.
        """
        return self._codes

    @property
    def codes(self) -> numpy.ndarray:
        """See :py:attr:`~get_codes`."""
        return self.get_codes()

    def get_levels(self) -> numpy.ndarray:
        """
        Returns:
            Array of strings containing the factor levels.
        """
        return self._levels

    @property
    def levels(self) -> numpy.ndarray:
        """See :py:attr:`~get_levels`."""
        return self.get_levels()

    def get_ordered(self) -> bool:
        """
        Returns:
            True if the levels are ordered, otherwise False.
        """
        return self._ordered

    @property
    def ordered(self) -> bool:
        """See :py:attr:`~get_ordered`."""
        return self.get_ordered()

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
        tmp = "Factor(codes=" + print_truncated_list(self._codes) + ", levels=" + print_truncated_list(self._levels))
        if self._ordered:
            tmp += ", ordered=True"
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
        message += "values: " + print_truncated_list(self._codes, transform=lambda i: self._levels[i]) + "\n"
        message += "levels: " + print_truncated_list(self._levels, transform=lambda x: x) + "\n"
        message += "ordered: " + str(self._ordered)
        return message

    def __getitem__(self, args: Union[int, bool, Sequence]) -> Union[str, "Factor"]:
        """Subset the ``Factor`` to the specified subset of indices.

        Args:
            args:
                Sequence of integers or booleans specifying the elements of
                interest. Alternatively, an integer/boolean scalar specifying a
                single element.

        Returns:
            If ``args`` is a sequence, returns same type as caller (a new
            ``Factor``) containing only the elements of interest from ``args``.

            If ``args`` is a scalar, a string is returned containing the
            level corresponding to the code at position ``args``. This may
            also be None if the code is missing.
        """
        args, scalar = normalize_subscript(args, len(self), None)
        if scalar:
            x = self._codes[args[0]]
            if x >= 0:
                return self._levels[x]
            else:
                return None 
        return type(self)(self._codes[args], self._levels, self._ordered, validate=False)

    def replace(self, sub: Sequence, value: Union[str, "Factor"], in_place: bool = False):
        """
        Replace items in the ``Factor`` list.  The ``subs`` elements in the
        current object are replaced with the corresponding values in ``value``.
        This is performed by finding the level for each entry of the
        replacement ``value``, matching it to a level in the current object,
        and replacing the entry of ``codes`` with the code of the matched
        level. If there is no matching level, a missing value is inserted.

        Args:
            args: 
                Sequence of integers or booleans specifying the items to be
                replaced.

            value: 
                If ``sub`` is a sequence, a ``Factor`` of the same length
                containing the replacement values.

            in_place:
                Whether the replacement should be performed on the current
                object.

        Returns:
            If ``in_place = False``, a new ``Factor`` is returned containing the
            contents of the current object after replacement by ``value``.

            If ``in_place = True``, the current object is returned after its
            items have been replaced.
        """
        sub, scalar = normalize_subscript(sub, len(self), None)
        codes = self._codes
        if not in_place:
            codes = codes.copy()

        if len(self._levels) == len(value._levels) and (self._levels == value._levels).all():
            for i, x in enumerate(sub):
                codes[x] = value._codes[i]
        else:
            mapping = match(value._levels, self._levels)
            for i, x in enumerate(args):
                v = value._codes[i]
                if v >= 0:
                    codes[x] = mapping[v]
                else:
                    codes[x] = -1

        if in_place:
            self._codes = codes
            return self
        else:
            return type(self)(codes, self._levels, self._ordered, validate=False)

    def __setitem__(self, args: Sequence[int], value: "Factor"):
        """See :py:attr:`~replace` for details."""
        return self.replace(args, value, in_place=True)

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
            new_codes = self._codes
        else:
            new_codes = self._codes.copy()

        in_use = [False] * len(self._levels)
        for x in self._codes:
            if x >= 0:
                in_use[x] = True

        new_levels = []
        reindex = [-1] * len(in_use)
        for i, x in enumerate(in_use):
            if x:
                reindex[i] = len(new_levels)
                new_levels.append(self._levels[i])
        new_levels = numpy.array(new_levels)

        for i, x in enumerate(self._codes):
            if not x >= 0:
                new_codes[i] = reindex[x]

        if in_place:
            self._codes = new_codes
            self._levels = new_levels
            return self
        else:
            current_class_const = type(self)
            return current_class_const(new_codes, new_levels, self._ordered, validate=False)

    def set_levels(self, levels: Union[str, List[str]], in_place: bool = False) -> "Factor":
        """Set or replace levels.

        Args:
            levels:
                A list of replacement levels. These should be unique strings
                with no missing values.

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
        lmapping = {}
        if isinstance(levels, str):
            new_levels = [levels]
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
            _check_levels_type(levels)
            new_levels = levels
            for i, x in enumerate(levels):
                if x in lmapping:
                    raise ValueError("levels should be unique")
                lmapping[x] = i

        mapping = [-1] * len(self._levels)
        for i, x in enumerate(self._levels):
            if x in lmapping:
                mapping[i] = lmapping[x]

        if in_place:
            new_codes = self._codes
        else:
            new_codes = self._codes.copy()
        for i, x in enumerate(new_codes):
            if x >= 0:
                new_codes[i] = mapping[x]
            else:
                new_codes[i] = -1

        if in_place:
            self._codes = new_codes
            self._levels = new_levels
            return self
        else:
            current_class_const = type(self)
            return current_class_const(new_codes, new_levels, self._ordered, validate=False)

    @levels.setter
    def levels(self, levels: Union[str, List[str]]):
        """See :py:attr:`~set_levels`."""
        warn("Setting property 'levels'is an in-place operation, use 'set_levels' instead", UserWarning)
        self.set_levels(levels, in_place=True)

    def __copy__(self) -> "Factor":
        """
        Returns:
            A shallow copy of the ``Factor`` object.
        """
        current_class_const = type(self)
        return current_class_const(self._codes, self._levels, self._ordered, validate=False)

    def __deepcopy__(self, memo) -> "Factor":
        """
        Returns:
            A deep copy of the ``Factor`` object.
        """
        current_class_const = type(self)
        return current_class_const(
            deepcopy(self._codes, memo),
            deepcopy(self._levels, memo),
            self._ordered,
            validate=False,
        )

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
        levels, indices = factorize(values, levels=levels, sort_levels=sort_levels)
        return Factor(indices, levels=levels, ordered=ordered)
