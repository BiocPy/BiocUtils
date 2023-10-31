from typing import Optional, List, Callable, Dict


def print_truncated(x, truncated_to: int = 3, full_threshold: int = 10) -> str:
    """
    Pretty-print an object, replacing the middle elements of lists/dictionaries
    with an ellipsis if there are too many. This provides a useful preview of
    an object without spewing out all of its contents on the screen.

    Args:
        x: Object to be printed.

        truncated_to:
            Number of elements to truncate to, at the start and end of the list
            or dictionary. This should be less than half of ``full_threshold``.

        full_threshold:
            Threshold on the number of elements, below which the list or
            dictionary is shown in its entirety.

    Returns:
        String containing the pretty-printed contents.
    """
    if isinstance(x, dict):
        return print_truncated_dict(x, truncated_to=truncated_to, full_threshold=full_threshold)
    elif isinstance(x, list):
        return print_truncated_list(x, truncated_to=truncated_to, full_threshold=full_threshold)
    else:
        return repr(x)


def print_truncated_list(x: List, truncated_to: int = 3, full_threshold: int = 10, transform: Optional[Callable] = None, sep: str = ", ", include_brackets: bool = True) -> str:
    """
    Pretty-print a list, replacing the middle elements with an ellipsis if
    there are too many. This provides a useful preview of an object without
    spewing out all of its contents on the screen.

    Args:
        x: List to be printed.

        truncated_to:
            Number of elements to truncate to, at the start and end of the
            list. This should be less than half of ``full_threshold``.

        full_threshold:
            Threshold on the number of elements, below which the list is
            shown in its entirety.

        transform:
            Optional transformation to apply to the elements of ``x``
            after truncation but before printing. Defaults to
            :py:meth:`~print_truncated` if not supplied.

        sep:
            Separator between elements in the printed list.

        include_brackets:
            Whether to include the start/end brackets.

    Returns:
        String containing the pretty-printed truncated list. 
    """
    collected = []
    if transform is None:
        transform = lambda y : print_truncated(y, truncated_to=truncated_to, full_threshold=full_threshold)

    if len(x) > full_threshold and len(x) > truncated_to * 2:
        for i in range(truncated_to):
            collected.append(transform(x[i]))
        collected.append("...")
        for i in range(truncated_to, 0, -1):
            collected.append(transform(x[len(x) - i]))
    else:
        for c in x:
            collected.append(transform(c))

    output = sep.join(collected)
    if include_brackets:
        output = "[" + output + "]"
    return output


def print_truncated_dict(x: Dict, truncated_to: int = 3, full_threshold: int = 10, transform: Optional[Callable] = None, sep: str = ", ", include_brackets: bool = True) -> str:
    """
    Pretty-print a dictionary, replacing the middle elements with an ellipsis
    if there are too many. This provides a useful preview of an object without
    spewing out all of its contents on the screen.

    Args:
        x: Dictionary to be printed.

        truncated_to:
            Number of elements to truncate to, at the start and end of the
            sequence. This should be less than half of ``full_threshold``.

        full_threshold:
            Threshold on the number of elements, below which the list is
            shown in its entirety.

        transform:
            Optional transformation to apply to the values of ``x`` after
            truncation but before printing. Defaults to
            :py:meth:`~print_truncated` if not supplied.

        sep:
            Separator between elements in the printed list.

        include_brackets:
            Whether to include the start/end brackets.

    Returns:
        String containing the pretty-printed truncated dict.
    """
    collected = []
    if transform is None:
        transform = lambda y : print_truncated(y, truncated_to=truncated_to, full_threshold=full_threshold)

    all_keys = x.keys()
    if len(x) > full_threshold and len(x) > truncated_to * 2:
        all_keys = list(all_keys)
        for i in range(truncated_to):
            collected.append(repr(all_keys[i]) + ": " + transform(x[all_keys[i]]))
        collected.append("...")
        for i in range(len(x) - truncated_to, len(x)):
            collected.append(repr(all_keys[i]) + ": " + transform(x[all_keys[i]]))
    else:
        for c in all_keys:
            collected.append(repr(c) + ": " + transform(x[c]))

    output = sep.join(collected)
    if include_brackets:
        output = "{" + output + "}"
    return output
