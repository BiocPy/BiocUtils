from __future__ import annotations

import copy
from typing import Any, Dict, Optional, Union
from warnings import warn

try:
    from typing import Self
except ImportError:
    from typing import TypeVar

    Self = TypeVar("Self", bound="BiocObject")

from .NamedList import NamedList

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "MIT"


def sanitize_metadata(metadata: Any) -> NamedList:
    """Sanitize metadata input to a NamedList."""
    if metadata is None:
        return NamedList()
    if isinstance(metadata, NamedList):
        return metadata
    if isinstance(metadata, dict):
        return NamedList.from_dict(metadata)

    raise TypeError(f"`metadata` must be a dictionary or NamedList, provided {type(metadata).__name__}.")


def _validate_metadata(metadata: Any) -> None:
    """Validate that metadata is of the correct type."""
    if not isinstance(metadata, (dict, NamedList)):
        raise TypeError(f"`metadata` must be a dictionary or NamedList, provided {type(metadata).__name__}.")


class BiocObject:
    """Base class for all BiocPy classes.

    Provides a standardized `metadata` slot and copy-on-write semantics.
    """

    def __init__(self, metadata: Optional[Union[Dict[str, Any], NamedList]] = None, validate: bool = True) -> None:
        """Initialize the BiocObject.

        Args:
            metadata:
                Additional metadata. Defaults to an empty NamedList.

            validate:
                Whether to validate the input. Defaults to True.
        """
        if validate and metadata is not None:
            _validate_metadata(metadata)

        self._metadata = sanitize_metadata(metadata)

    def _define_output(self, in_place: bool = False) -> Self:
        """Internal utility to handle in-place vs copy-on-modify."""
        if in_place:
            return self
        else:
            return copy.copy(self)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        meta_len = len(self._metadata)
        return f"<{class_name}> with {meta_len} metadata elements"

    ##########################
    ######>> Metadata <<######
    ##########################

    @property
    def metadata(self) -> NamedList:
        """Get the metadata.

        Returns:
            NamedList of metadata.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Optional[Union[Dict[str, Any], NamedList]]) -> None:
        """Set metadata in-place."""
        warn(
            "Setting property 'metadata' is an in-place operation, use 'set_metadata' instead",
            UserWarning,
        )
        self.set_metadata(metadata=metadata, in_place=True)

    def get_metadata(self) -> NamedList:
        """Alias for :py:attr:`~metadata` getter."""
        return self.metadata

    def set_metadata(self, metadata: Optional[Union[Dict[str, Any], NamedList]], in_place: bool = False) -> Self:
        """Set new metadata.

        Args:
            metadata:
                New metadata for this object.

            in_place:
                Whether to modify the object in place.
                Defaults to False (returns a copy).

        Returns:
            A modified object, either as a copy of the original
            or as a reference to the (in-place-modified) original.
        """
        if metadata is not None:
            _validate_metadata(metadata)

        output = self._define_output(in_place)
        output._metadata = sanitize_metadata(metadata)
        return output
