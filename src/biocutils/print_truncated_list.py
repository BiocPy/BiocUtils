from typing import Optional, Sequence, Callable


def print_truncated_list(x: Sequence, truncated_to = 3, full_threshold = 10, transform: Optional[Callable] = None, sep: str = ", ", include_brackets: bool = True) -> str:
    """
    Pretty-print a truncated list, replacing the middle elements with an
    ellipsis if there are too many. This provides a useful preview of an
    object without spewing out all of its contents on the screen.

    Args:
        x: List or some other sequence to be printed.

        truncated_to:
            Number of elements to truncate to, at the start and end of the
            sequence. This should be less than half of ``full_threshold``.

        full_threshold:
            Threshold on the number of elements, below which the list is
            shown in its entirety.

        transform:
            Optional transformation to apply to the elements of ``x``
            after truncation but before printing.

        sep:
            Separator between elements in the printed list.

        include_brackets:
            Whether to include the start/end brackets.

    Returns:
        String containing the pretty-printed truncated list. 
    """
    collected = []
    if transform is None:
        transform = lambda y : y

    if len(x) > full_threshold and len(x) > truncated_to * 2:
        for i in range(truncated_to):
            collected.append(repr(transform(x[i])))
        collected.append("...")
        for i in range(truncated_to, 0, -1):
            collected.append(repr(transform(x[len(x) - i])))
    else:
        for c in x:
            collected.append(repr(transform(c)))

    output = sep.join(collected)
    if include_brackets:
        output = "[" + output + "]"
    return output
