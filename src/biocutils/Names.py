from typing import Sequence, Optional, Iterable, Union, Any


class Names(list):
    """
    List of strings containing names. Typically used to decorate sequences,
    such that callers can get or set elements by name instead of position.
    """

    def __init__(self, iterable: Optional[Iterable] = None, coerce: bool = True):
        """
        Args:
            iterable:
                Some iterable object containing strings, or values that can
                be coerced into strings.

            coerce:
                Whether to coerce values of ``iterable`` into strings.
        """
        if iterable is None:
            super().__init__()
        elif coerce and not isinstance(iterable, type(self)):
            super().__init__(str(y) for y in iterable)
        else:
            super().__init__(iterable)
        self._reverse = None

    # Enable fast indexing by name, but only on demand. This reverse mapping
    # field is strictly internal and should be completely transparent to the
    # user; so, calls to map() can be considered as 'non-mutating', as it
    # shouldn't manifest in any visible changes to the Names object. I guess
    # that things become a little hairy in multi-threaded contexts where I
    # should probably protect the final assignment to _reverse. But then
    # again, Python is single-threaded anyway, so maybe it doesn't matter.
    def _populate_reverse_index(self):
        if self._reverse is None:
            revmap = {}
            for i, n in enumerate(self):
                if n not in revmap:
                    revmap[n] = i
            self._reverse = revmap

    def _wipe_reverse_index(self):
        self._reverse = None
    
    def __getitem__(self, index: Union[int, slice]) -> Union[str, "Names"]:
        """
        Args:
            index:
                Integer specifying the position of interest, or a slice 
                specifying multiple such positions.

        Returns:
            If ``index`` is a slice, a new ``Names`` object is returned
            containing names from the specified positions.

            If ``index`` is an integer, the name at that position is returned.
        """
        output = super().__getitem__(index)
        if isinstance(index, slice):
            return Names(output, coerce=False)
        return output

    def __setitem__(self, index: Union[int, slice], item: Any):
        """
        Args:
            index:
                Integer specifying the position of interest, or a slice
                specifying multiple such positions.

            item:
                If ``index`` is an integer, a string containing a name.

                If ``index`` is a slice, an iterable object of the appropriate
                length, containing strings to use as replacement names.

        Returns:
            The current object is modified with the replacement names.
        """
        self._wipe_reverse_index()
        if isinstance(index, slice):
            new_it = item
            if not isinstance(item, type(self)):
                new_it = (str(x) for x in item)
            super().__setitem__(index, new_it)
        else:
            super().__setitem__(index, str(item))

    def map(self, name: str) -> int:
        """
        Args:
            name: Name of interest.

        Returns:
            Index containing the position of the first occurrence of ``name``;
            or -1, if ``name`` is not present in this object.
        """
        self._populate_reverse_index()
        if name in self._reverse:
            return self._reverse[name]
        else:
            return -1

    def append(self, name: Any):
        """
        Args:
            name: Name to be added.

        Returns:
            ``name`` is added to the current object.
        """
        name = str(name)
        if self._reverse is not None and name not in self._reverse:
            self._reverse[name] = len(self)
        super().append(name)

    def insert(self, index: int, name: str):
        """
        Args:
            index: Position on the object to insert at.

            name: Name to be added.

        Returns:
            ``name`` is inserted into the current object before ``index``.
        """
        self._wipe_reverse_index()
        super().insert(index, str(name))

    def extend(self, names: Sequence[str]):
        """
        Args:
            names: Names to add to the current object.

        Returns:
            ``names`` are added to the current object.
        """
        if self._reverse is not None:
            for i, n in enumerate(names):
                n = str(n)
                if n not in self._reverse:
                    self._reverse[n] = i + len(self)
                self.append(n)
        elif isinstance(names, Names):
            super().extend(names)
        else:
            super().extend(str(y) for y in names)

    def __add__(self, other: list):
        """
        Args:
            other: List of names.

        Returns:
            A new ``Names`` containing the combined contents
            of the current object and ``other``.
        """
        output = self.copy()
        output.extend(other)
        return output

    def __iadd__(self, other: list):
        """
        Args:
            other: List of names.

        Returns:
            The current object is modified by adding ``other`` to its names.
        """
        self.extend(other)
        return self

    def copy(self):
        """
        Returns:
            A copy of the current object.
        """
        return Names(self, coerce=False)


def _combine_names(*x: Any, get_names: Callable) -> Union[Names, None]:
    all_names = []
    has_names = False
    for y in x:
        n = get_names(y)
        if n is None:
            all_names.append(len(x))
        else:
            has_names = True
            all_names.append(n)

    if not has_names:
        return None
    else:
        output = Names()
        for i, n in enumerate(all_names):
            if not isinstance(n, Names):
                output.extend([""] * n)
            else:
                output.extend(n)
        return output
