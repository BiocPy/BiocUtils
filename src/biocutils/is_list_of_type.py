from typing import Any

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def is_list_of_type(x: Any, target_type) -> bool:
    """Checks if ``x`` is a list, and whether all elements of the list are of the same type.

    Args:
        x (Any): Any list-like object.
        target_type (callable): Type to check for, e.g. ``str``, ``int``.

    Returns:
        bool: True if ``x`` is :py:class:`list` or :py:class:`tuple` and
        all elements are of the same type.
    """
    return isinstance(x, (list, tuple)) and all(
        isinstance(item, target_type) for item in x
    )
