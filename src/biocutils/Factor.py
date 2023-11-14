from copy import deepcopy
from typing import List, Sequence, Union, Optional
from warnings import warn
import numpy

from .StringList import StringList
from .Names import Names
from .match import match
from .factorize import factorize
from .normalize_subscript import normalize_subscript
from .is_missing_scalar import is_missing_scalar
from .print_truncated import print_truncated_list
from .subset_sequence import subset_sequence
from .combine_sequences import combine_sequences
from .is_list_of_type import is_list_of_type


class Factor:
    """Factor class, equivalent to R's ``factor``.

    This is a vector of integer codes, each of which is an index into a list of
    unique strings. The aim is to encode a list of strings as integers for
    easier numerical analysis.
    """

    def __init__(self, codes: Sequence[int], levels: Sequence[str], ordered: bool = False, names: Optional[Names] = None, validate: bool = True):
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

            validate:
                Whether to validate the arguments. Internal use only.
        """
        if not isinstance(codes, numpy.ndarray):
            replacement = numpy.ndarray(len(codes), dtype=numpy.min_scalar_type(-len(levels))) # get a signed type.
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
                codes = codes.astype(numpy.min_scalar_type(-len(levels)))

        if not isinstance(levels, StringList):
            levels = StringList(levels)

        self._codes = codes
        self._levels = levels
        self._ordered = bool(ordered)

        if names is not None:
            if not isinstance(names, Names):
                names = Names(names)
            if len(names) != len(codes):
                raise ValueError("'names' and 'codes' should have the same length")
        self._names = names

        if validate:
            if any(x is None for x in levels):
                raise TypeError("all entries of 'levels' should be non-missing")
            if len(set(levels)) < len(levels):
                raise ValueError("all entries of 'levels' should be unique")
            for x in codes:
                if x < -1 or x >= len(self._levels):
                    raise ValueError("all entries of 'codes' should refer to an entry of 'levels'")


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

    def get_levels(self) -> StringList:
        """
        Returns:
            List of strings containing the factor levels.
        """
        return self._levels

    @property
    def levels(self) -> StringList:
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

    def get_names(self) -> Union[None, Names]:
        """
        Returns:
            List of names, or None if no names are available.
        """
        return 

    @property
    def names(self) -> Union[None, Names]:
        """See :py:attr:`~get_names`."""
        return self.get_names()

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
        if self._names is not None:
            tmp += ", names=" + repr(self._names)
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
        message += "levels: " + print_truncated_list(self._levels, transform=lambda x: x, include_brackets=False) + "\n"
        if self._names is not None:
            message += "names: " + print_truncated_list(self._names, transform=lambda x: x, include_brackets=False) + "\n"
        message += "ordered: " + str(self._ordered)
        return message

    def __getitem__(self, sub: Union[int, bool, str, Sequence]) -> Union[str, "Factor"]:
        """Subset the ``Factor`` to the specified subset of indices.

        Args:
            sub:
                Sequence specifying the elements of interest. Alternatively, a
                scalar specifying a single element. For more details, see
                :py:func:`~normalize_subscript.normalize_subscript`.

        Returns:
            If ``sub`` is a sequence, returns same type as caller (a new
            ``Factor``) containing only the elements of interest from ``sub``.

            If ``sub`` is a scalar, a string is returned containing the
            level corresponding to the code at position ``sub``. This may
            also be None if the code is missing.
        """
        sub, scalar = normalize_subscript(sub, len(self), self._names)
        if scalar:
            x = self._codes[sub[0]]
            if x >= 0:
                return self._levels[x]
            else:
                return None 
        return type(self)(self._codes[sub], levels=self._levels, ordered=self._ordered, names=subset_sequence(self._names, sub), validate=False)

    def replace(self, sub: Union[int, str, bool, Sequence], value: Union[str, "Factor"], in_place: bool = False):
        """
        Replace items in the ``Factor`` list.  The ``sub`` elements in the
        current object are replaced with the corresponding values in ``value``.
        This is performed by finding the level for each entry of the
        replacement ``value``, matching it to a level in the current object,
        and replacing the entry of ``codes`` with the code of the matched
        level. If there is no matching level, a missing value is inserted.

        Args:
            sub: 
                Sequence or scalar specifying the items to be replaced, see
                :py:func:`~normalize_subscript.normalize_subscript`.

            value: 
                If ``sub`` is a sequence, a ``Factor`` of the same length
                containing the replacement values.

                If ``sub`` is a scalar, a string corresponding to one of the
                levels, or None to represent a missing value..

            in_place:
                Whether the replacement should be performed on the current
                object.

        Returns:
            If ``in_place = False``, a new ``Factor`` is returned containing the
            contents of the current object after replacement by ``value``.

            If ``in_place = True``, the current object is returned after its
            items have been replaced.
        """
        codes = self._codes
        if not in_place:
            codes = codes.copy()

        sub, scalar = normalize_subscript(sub, len(self), self._names)
        if scalar:
            chosen = -1
            for i, x in enumerate(value._levels):
                if x == value:
                    chosen = i
                    break
            codes[sub[0]] = chosen
        else:
            if self._levels == value._levels:
                for i, x in enumerate(sub):
                    codes[x] = value._codes[i]
            else:
                mapping = match(value._levels, self._levels)
                for i, x in enumerate(sub):
                    v = value._codes[i]
                    if v >= 0:
                        codes[x] = mapping[v]
                    else:
                        codes[x] = -1

        if in_place:
            self._codes = codes
            return self
        else:
            return type(self)(codes, levels=self._levels, ordered=self._ordered, names=self._names, validate=False)

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

        new_levels = StringList([])
        reindex = [-1] * len(in_use)
        for i, x in enumerate(in_use):
            if x:
                reindex[i] = len(new_levels)
                new_levels.append(self._levels[i])

        for i, x in enumerate(self._codes):
            if x >= 0:
                new_codes[i] = reindex[x]

        if in_place:
            self._codes = new_codes
            self._levels = new_levels
            return self
        else:
            current_class_const = type(self)
            return current_class_const(new_codes, levels=new_levels, ordered=self._ordered, names=self._names, validate=False)

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
            return current_class_const(new_codes, levels=new_levels, ordered=self._ordered, names=self._names, validate=False)

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
        return current_class_const(self._codes, levels=self._levels, ordered=self._ordered, names=self._names, validate=False)

    def __deepcopy__(self, memo) -> "Factor":
        """
        Returns:
            A deep copy of the ``Factor`` object.
        """
        current_class_const = type(self)
        return current_class_const(
            deepcopy(self._codes, memo),
            levels=deepcopy(self._levels, memo),
            ordered=self._ordered,
            names=deepcopy(self._names, memo),
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
    def from_sequence(x: Sequence[str], levels: Optional[Sequence[str]] = None, sort_levels: bool = True, ordered: bool = False, names: Optional[Names] = None) -> "Factor":
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
        return Factor(indices, levels=levels, ordered=ordered, names=names)


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
        new_levels = []
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

    new_names = None

    return Factor(combine_sequences(*new_codes), levels=new_levels, ordered=new_ordered, validate=False)
