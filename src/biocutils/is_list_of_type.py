from typing import Callable, Union

import numpy as np
import numpy.ma as ma

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def is_list_of_type(x: Union[list, tuple], target_type: Callable, ignore_none: bool = False) -> bool:
    """Checks if ``x`` is a list, and whether all elements of the list are of the same type.

    Args:
        x:
            A list or tuple of values.

        target_type:
            Type to check for, e.g. ``str``, ``int``.

        ignore_none:
            Whether to ignore Nones when comparing to ``target_type``.

    Returns:
        True if ``x`` is a list or tuple and all elements are of the target
        type (or None, if ``ignore_none = True``). Otherwise, False.
    """
    if not isinstance(x, (list, tuple, np.ndarray, ma.MaskedArray)):
        return False

    if isinstance(x, ma.MaskedArray):
        if not ignore_none:
            return all(x.mask) and all(isinstance(item, target_type) for item in x.data)
        else:
            return all(isinstance(item, target_type) for item in x.data[x.mask])

    if not ignore_none:
        return all(isinstance(item, target_type) for item in x)

    return all((isinstance(item, target_type) or item is None) for item in x)
